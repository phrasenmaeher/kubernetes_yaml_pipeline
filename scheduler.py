import argparse
from subprocess import run, PIPE
from typing import Any


def get_experiments(experiment_number: int = -1) -> dict[Any, Any]:
    """
    Returns a dictionary of experiments to run. Note that these are just arbitrary examples.
    :param experiment_number: The experiment number to run. If -1, run all experiments.
    :return: A dictionary of experiments to run.
    """
    experiments = {1: {"batch_size": 32, "epochs": 100, "model": "resnet18", "dataset": "cifar10"},
                   2: {"batch_size": 64, "epochs": 100, "model": "resnet18", "dataset": "omniglot"},
                   3: {"batch_size": 32, "epochs": 50, "model": "resnet152", "dataset": "animals"},
                   4: {"batch_size": 64, "epochs": 50, "model": "resnet152", "dataset": "flowers"},
                   }
    if experiment_number != -1:
        return {experiment_number: experiments[experiment_number]}
    return experiments


def schedule(args) -> None:
    """
    Schedules the experiments to run.
    :param args: The commandline arguments.
    :return: Nothing.
    """
    with open("template.yaml", "r") as f:
        config_string = "".join(f.readlines())

    experiments = get_experiments(args.specific_experiment)
    image = "your-container-registry/your-image:latest"
    directory_to_mount = "/some/directory/to/mount"
    dataset_directory = "/some/directory/with/datasets"
    for k, v in experiments.items():
        print(f"---Running experiment {k}---")
        study_name = str(k)
        res = config_string.format(
            study_name,  # {0}
            v["model"],  # {1}
            v["batch_size"],  # {2}
            v["dataset"],  # {3}
            v["epochs"],  # {4}
            directory_to_mount,  # {5}
            image,  # {6}
            dataset_directory,  # {7}
        )
        print(res)  # print the config file

        # Note that this is just an example, and no actual job will be started or terminated
        if args.delete_only:
            # only delete the job (if it exists)
            output = run(["bash", "delete.sh", res], stdout=PIPE)
            print(output.stdout.decode("utf-8").strip())
        else:
            # first, delete old job with same name
            output = run(["bash", "delete.sh", res], stdout=PIPE)
            print(output.stdout.decode("utf-8").strip())
            # then, create new job
            output = run(["bash", "schedule.sh", res], stdout=PIPE)
            print(output.stdout.decode("utf-8").strip())


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--specific-experiment", dest="specific_experiment", type=int, default=-1)
    argument_parser.add_argument("--delete-only", dest="delete_only", action="store_true")
    args = argument_parser.parse_args()
    schedule(args)
