<?php

function executeCommand($command)
{
    $output = "";
    $error = "";

    // Execute the command
    exec($command, $outputLines, $returnCode);

    // Capture the command output
    $output = implode("\n", $outputLines);

    // Check for any errors
    if ($returnCode !== 0) {
        $error = "Error executing command: " . $command;
    }

    return [$output, $error];
}

function main()
{
    echo "<h1>Git & Docker Commands</h1>";

    $menu = ["Status", "Add", "Commit", "Push", "Pull", "Branch", "Checkout", "Merge", "Log", "Remote", "Intro", "Directory Visualizer", "Docker Build & Push"];
    $choice = $_POST["activity"] ?? "Intro";

    if ($choice == "Status") {
        echo "<h2>Status</h2>";
        $command = "git status";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Add") {
        echo "<h2>Add</h2>";
        $filePath = $_POST["file_path"] ?? "";
        $command = "git add $filePath";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Commit") {
        echo "<h2>Commit</h2>";
        $commitMessage = $_POST["commit_message"] ?? "";
        $command = "git commit -m '$commitMessage'";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Push") {
        echo "<h2>Push</h2>";
        $command = "git push";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Pull") {
        echo "<h2>Pull</h2>";
        $command = "git pull";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Branch") {
        echo "<h2>Branch</h2>";
        $command = "git branch";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Checkout") {
        echo "<h2>Checkout</h2>";
        $branchName = $_POST["branch_name"] ?? "";
        $command = "git checkout $branchName";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Merge") {
        echo "<h2>Merge</h2>";
        $branchName = $_POST["branch_name"] ?? "";
        $command = "git merge $branchName";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Log") {
        echo "<h2>Log</h2>";
        $command = "git log";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Remote") {
        echo "<h2>Remote</h2>";
        $command = "git remote -v";
        [$output, $error] = executeCommand($command);

        if (!empty($error)) {
            echo "<p>Error: $error</p>";
        } else {
            echo "<pre>$output</pre>";
        }
    } elseif ($choice == "Intro") {
        echo "<h2>Intro</h2>";
        // Add your code for the "Intro" section here
    } elseif ($choice == "Directory Visualizer") {
        echo "<h2>Directory Visualizer</h2>";

        // Get the current directory
        $directory = dirname(__FILE__);

        // Get all the files in the directory
        $files = scandir($directory);

        // Remove . and .. from the list
        $files = array_diff($files, array('.', '..'));

        // Display the files
        echo "<ul>";
        foreach ($files as $file) {
            echo "<li>$file</li>";
        }
        echo "</ul>";
    } elseif ($choice == "Docker Build & Push") {
        echo "<h2>Docker Build & Push</h2>";
        // Add your code for the "Docker Build & Push" section here
        $dockerfilePath = $_POST["dockerfile_path"] ?? "Dockerfile";
        $imageTag = $_POST["image_tag"] ?? "";

        // Build the Docker image
        $buildCommand = "docker build -t $imageTag -f $dockerfilePath .";
        [$buildOutput, $buildError] = executeCommand($buildCommand);

        if (!empty($buildError)) {
            echo "<p>Error during Docker build: $buildError</p>";
        } else {
            echo "<pre>$buildOutput</pre>";

            // Push the Docker image
            $pushCommand = "docker push $imageTag";
            [$pushOutput, $pushError] = executeCommand($pushCommand);

            if (!empty($pushError)) {
                echo "<p>Error during Docker push: $pushError</p>";
            } else {
                echo "<pre>$pushOutput</pre>";
            }
        }
    }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    main();
} else {
?>

<html>
<head>
    <title>Git & Docker Commands</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }

        h1, h2 {
            margin-bottom: 10px;
        }

        pre {
            background-color: #f5f5f5;
            padding: 10px;
        }

        label {
            font-weight: bold;
            margin-right: 10px;
        }

        select {
            margin-right: 10px;
        }

        input[type="text"] {
            margin-right: 10px;
        }

        input[type="submit"] {
            padding: 5px 10px;
        }
    </style>

    <script>
        function showActivity() {
            var activitySelect = document.getElementById("activity");
            var selectedActivity = activitySelect.value;
            var form = document.getElementById("commandForm");

            if (selectedActivity === "Status" || selectedActivity === "Add" || selectedActivity === "Commit" ||
                selectedActivity === "Push" || selectedActivity === "Pull" || selectedActivity === "Branch" ||
                selectedActivity === "Checkout" || selectedActivity === "Merge" || selectedActivity === "Log" ||
                selectedActivity === "Remote" || selectedActivity === "Docker Build & Push") {
                form.style.display = "block";
            } else {
                form.style.display = "none";
            }
        }
    </script>
</head>
<body>
    <h1>Git & Docker Commands</h1>

    <form id="commandForm" method="POST" action="" style="display: none;">
        <label for="activity">Select Activity:</label>
        <select id="activity" name="activity" onchange="showActivity()">
            <option value="Status">Status</option>
            <option value="Add">Add</option>
            <option value="Commit">Commit</option>
            <option value="Push">Push</option>
            <option value="Pull">Pull</option>
            <option value="Branch">Branch</option>
            <option value="Checkout">Checkout</option>
            <option value="Merge">Merge</option>
            <option value="Log">Log</option>
            <option value="Remote">Remote</option>
            <option value="Intro">Intro</option>
            <option value="Directory Visualizer">Directory Visualizer</option>
            <option value="Docker Build & Push">Docker Build & Push</option>
        </select>

        <div id="filePathInput" style="display: none;">
            <label for="file_path">File Path:</label>
            <input type="text" id="file_path" name="file_path">
        </div>

        <div id="commitMessageInput" style="display: none;">
            <label for="commit_message">Commit Message:</label>
            <input type="text" id="commit_message" name="commit_message">
        </div>

        <div id="branchNameInput" style="display: none;">
            <label for="branch_name">Branch Name:</label>
            <input type="text" id="branch_name" name="branch_name">
        </div>

        <div id="imageTagInput" style="display: none;">
            <label for="image_tag">Image Tag:</label>
            <input type="text" id="image_tag" name="image_tag">
        </div>

        <div id="dockerfilePathInput" style="display: none;">
            <label for="dockerfile_path">Dockerfile Path:</label>
            <input type="text" id="dockerfile_path" name="dockerfile_path" value="Dockerfile">
        </div>

        <input type="submit" value="Submit">
    </form>

    <script>
        showActivity();
    </script>
</body>
</html>

<?php
}
?>
