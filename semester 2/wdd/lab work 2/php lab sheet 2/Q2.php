<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello There</title>
</head>
<body>
    <h1>Hello There</h1>

    <?php
    echo "<p style='color: green;'>Welcome to learn PHP</p>";

    $php_features = [
        "PHP is a server scripting language, and a powerful tool for making dynamic and interactive Web pages.",
        "PHP is a widely-used, free, and efficient alternative to competitors such as Microsoft's ASP"
    ];

    echo "<ul>";
    foreach ($php_features as $feature) {
        echo "<li>$feature</li>";
    }
    echo "</ul>";
    ?>
</body>
</html>