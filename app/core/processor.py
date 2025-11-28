"""Centralized batch processing engine"""
import pandas as pd
import concurrent.futures
from typing import List, Callable, Optional
from tqdm import tqdm

from ..models.schemas import ClassificationTask, ClassificationResult, ProcessingStats
from ..utils.text_utils import merge_feedback, normalize_feedback_key, split_label
from .cache_manager import CacheManager
from .classifier import Classifier


class CentralProcessor:
    """Centralized processor for batch classification tasks"""
    
    def __init__(self, classifier: Classifier, cache_manager: CacheManager, 
                 max_workers: int = 10):
        self.classifier = classifier
        self.cache_manager = cache_manager
        self.max_workers = max_workers
    
    def prepare_tasks(self, df: pd.DataFrame) -> List[ClassificationTask]:
        """Prepare classification tasks from DataFrame"""
        tasks = []
        for idx, row in df.iterrows():
            feedback = merge_feedback(row)
            if not feedback:
                continue
            
            feedback_key = normalize_feedback_key(feedback)
            tasks.append(ClassificationTask(
                index=idx,
                feedback=feedback,
                feedback_key=feedback_key
            ))
        
        return tasks
    
    def process_task(self, task: ClassificationTask) -> ClassificationResult:
        """Process a single classification task"""
        # Check cache first
        cached_label = self.cache_manager.get(task.feedback_key)
        if cached_label:
            split_labels = split_label(cached_label)
            return ClassificationResult(
                index=task.index,
                label_en=cached_label,
                status='hit',
                feedback_key=task.feedback_key,
                **split_labels
            )
        
        # Call LLM classifier
        label = self.classifier.classify(task.feedback)
        
        if label:
            # Update cache
            self.cache_manager.set(task.feedback_key, label)
            split_labels = split_label(label)
            return ClassificationResult(
                index=task.index,
                label_en=label,
                status='miss',
                feedback_key=task.feedback_key,
                **split_labels
            )
        else:
            return ClassificationResult(
                index=task.index,
                label_en=None,
                label_1=None,
                label_2=None,
                label_3=None,
                label_4=None,
                status='failed',
                feedback_key=task.feedback_key
            )
    
    def process_batch(self, tasks: List[ClassificationTask], 
                     progress_callback: Optional[Callable] = None) -> tuple[List[ClassificationResult], ProcessingStats]:
        """Process batch of tasks with concurrent execution"""
        results = []
        stats = ProcessingStats(total_tasks=len(tasks))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.process_task, task): task for task in tasks}
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    result = future.result()
                    results.append(result)
                    stats.update(result.status)
                    
                    # Progress callback
                    if progress_callback:
                        progress_callback(i + 1, len(tasks))
                
                except Exception as e:
                    print(f"Worker exception: {e}")
        
        # Sort results by index
        results.sort(key=lambda x: x.index)
        
        # Save cache after batch processing
        self.cache_manager.save()
        
        return results, stats
    
    def apply_results_to_dataframe(self, df: pd.DataFrame, 
                                   results: List[ClassificationResult]) -> pd.DataFrame:
        """Apply classification results to DataFrame"""
        df_out = df.copy()
        
        # Initialize columns
        for col in ["label_en", "label_1", "label_2", "label_3", "label_4"]:
            if col not in df_out.columns:
                df_out[col] = None
        
        # Apply results
        for result in results:
            if result.label_en:
                df_out.at[result.index, "label_en"] = result.label_en
                df_out.at[result.index, "label_1"] = result.label_1
                df_out.at[result.index, "label_2"] = result.label_2
                df_out.at[result.index, "label_3"] = result.label_3
                df_out.at[result.index, "label_4"] = result.label_4
        
        return df_out
