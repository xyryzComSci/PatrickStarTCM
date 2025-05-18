import os
import re
import csv
from glob import glob


def main():
    rows = list()
    for tcm in glob("*.csv"):
        with open(tcm, newline="") as file:
            rows = list(csv.reader(file))
        break

    SNAKECASE = re.compile(r"[^\w.]+")
    SAFE_PATH = re.compile(r"[^\w\-. ]+")

    read_me = []
    read_me.append("# ishiraTCM")
    read_me.append(
        "> This repository contains all test cases for PawsMatch, organized by feature module.  \n\n"
    )
    read_me.append("## Test Cases  \n\n")

    path = []
    directory = ""
    for row in rows[1:]:
        assert len(row) == 3, "Invalid TCM file."

        test_case_name = row[0]
        test_case_id = row[1]
        test_case_summary = row[2]

        if not (test_case_id.strip() and test_case_summary.strip()):
            test_case_name = SAFE_PATH.sub("-", test_case_name)
            if test_case_name[0] != " ":
                path = [test_case_name.strip()]
                directory = "/".join(path).replace("\/\/", "/")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    read_me.append(f" * [{test_case_name}](<./{directory}>)  ")
                    print(directory)
                continue
            elif test_case_name[2] != " ":
                if len(path) == 3:
                    # Fix: Delete from highest index to lowest to avoid index errors
                    del path[2]  # Delete third element first
                    del path[1]  # Then delete second element
                elif len(path) == 2:
                    del path[1]
                path.append(test_case_name.strip())
                directory = "/".join(path).replace("\/\/", "/")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    read_me.append(f"   * [{test_case_name.strip()}](<./{directory}>)  ")
                    print(directory)
                continue
            elif test_case_name[4] != " ":
                if len(path) == 3:
                    del path[2]
                path.append(test_case_name.strip())
                directory = "/".join(path).replace("\/\/", "/")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    read_me.append(f"     * [{test_case_name.strip()}](<./{directory}>)  ")
                    print(directory)
                continue

            raise Exception("Unsupported file format.")

        test_case_name = test_case_name.strip()
        filename = SNAKECASE.sub("_", test_case_name.lower())
        filepath = f"{directory}/{test_case_id}_{filename}.md".replace("\/\/", "/")

        if os.path.exists(filepath):
            continue

        depth = " " * (len(path)*2)
        read_me.append(
            f"{depth} * [{test_case_id}: {test_case_name}](<./{filepath}>)  "
        )

        print(filepath)

        contents = (
            f"## **{test_case_id}:** {test_case_name}  \n\n"
            f"> **Summary:** {test_case_summary}  <br>\n\n"
            f"**Preconditions:** _None_  \n\n"
            f"Scenario 1 \n\n"
            f" | \# | Step | Expected Behavior | \n"
            f" |----|------|-------------------| \n"
            f" |  1 |      | Verify that ...   | \n"
            f" |  2 |      | Verify that ...   | \n"
            f" |  3 |      | Verify that ...   |  \n\n"
            f"**Post-conditions:**  \n\n"
            f" - x  \n"
            f" - y  \n"
            f" - z  \n"
        )

        with open(filepath, "w+", encoding="utf-8") as file:
            file.write(contents)

        with open("README.md", "w+", encoding="utf-8") as file:
            file.write("\n".join(read_me))


if __name__ == "__main__":
    main()