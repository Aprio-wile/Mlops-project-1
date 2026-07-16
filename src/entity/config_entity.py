from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataingestionConfig:
    root_dir: Path
    url: str
    data_path: Path
    request_timeout: int

@dataclass(frozen=True)
class DatapreprocessConfig:
    root_dir: Path
    data_path: Path
    test_size: float
    X_train_data_path: Path
    X_test_data_path: Path
    y_train_data_path: Path
    y_test_data_path: Path
    target_col: str
    col_to_drop: list
    label_pkl_path: Path
    preprocess_pkl_path: Path

@dataclass(frozen=True)
class DatavalidationConfig:
    root_dir: Path
    data_path: Path
    status_file: Path

@dataclass(frozen=True)
class modeltrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_path: Path
    methods: list
    X_train_data_path: Path
    X_test_data_path: Path
    y_train_data_path: Path
    y_test_data_path: Path   
    timeout: int
    n_trials: int
    score: str
    cv: int
    
@dataclass(frozen=True)
class modelevaluationConfig:
    root_dir: Path
    X_test_data_path: Path
    y_test_data_path: Path
    model_path: Path
    metric_path: Path


@dataclass(frozen=True)
class predictionpipelineConfig:
    model_path: Path
    label_pkl_path: Path
    preprocess_pkl_path: Path    