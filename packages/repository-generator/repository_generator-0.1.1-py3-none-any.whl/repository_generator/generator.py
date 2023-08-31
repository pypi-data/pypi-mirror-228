import os


def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")


def create_file(path: str, content: str = "") -> None:
    with open(path, "w") as file:
        file.write(content)
    print(f"Created file: {path}")
    print(f"File already exists: {path}")


def main() -> None:
    # project_name = "data_science_project"
    # # Create project root directory
    # create_directory(project_name)
    # os.chdir(project_name)
    root_dir = os.getcwd()
    os.chdir(root_dir)
    # Create subdirectories for config
    create_directory("config")
    create_directory("config/runtime_config")
    create_directory("config/data_config")
    create_directory("config/model_config")
    create_directory("config/plot_config")
    # Create subdirectories for data
    create_directory("data")
    create_directory("data/raw")
    create_directory("data/raw/external")
    create_directory("data/raw/internal")
    create_directory("data/processed")
    create_directory("data/final")
    # Create subdirectories for notebooks
    create_directory("notebooks")
    # Create subdirectories for outputs
    create_directory("output")
    create_directory("output/features")
    create_directory("output/models")
    create_directory("output/models/Experiments")
    create_directory("output/models/Final_Model")
    create_directory("output/reports")
    create_directory("output/reports/figures")
    # Create subdirectories for scripts
    create_directory("scripts")
    create_directory("scripts/data_processing")
    create_directory("scripts/feature_generation")
    create_directory("scripts/modeling")
    create_directory("scripts/model_evaluation")
    create_directory("scripts/visualization")
    # Create requirements.txt
    create_file("requirements.txt")
    # Create README.md
    readme_content = """
    Top Level Readme for the project
    """
    create_file("README.md", readme_content)
    # Create .gitignore
    gitignore_content = """
    data/raw/
    data/processed/
    data/external/
    models/
    reports/figures/
    .DS_Store
    """
    create_file(".gitignore", gitignore_content)


if __name__ == "__main__":
    main()
