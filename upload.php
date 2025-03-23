<?php
// Basic upload handler for demonstration (add security validations for production)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = $_POST['contentTitle'];
    $type = $_POST['contentType'];
    $description = $_POST['contentText'];

    // Handle file upload if a file was provided
    if (isset($_FILES['contentFile']) && $_FILES['contentFile']['error'] === 0) {
        $uploadDir = 'uploads/';
        if (!is_dir($uploadDir)) {
            mkdir($uploadDir, 0777, true);
        }
        $fileName = basename($_FILES['contentFile']['name']);
        $uploadFile = $uploadDir . $fileName;

        if (move_uploaded_file($_FILES['contentFile']['tmp_name'], $uploadFile)) {
            echo "File uploaded successfully: " . htmlspecialchars($fileName);
        } else {
            echo "Error uploading file.";
        }
    } else {
        echo "No file uploaded or file error.";
    }

    // Display submitted details for demo purposes
    echo "<br>Title: " . htmlspecialchars($title);
    echo "<br>Type: " . htmlspecialchars($type);
    echo "<br>Description: " . htmlspecialchars($description);
} else {
    echo "Invalid request.";
}
?>
