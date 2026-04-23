<?php
// Database Connection
$conn = new mysqli("localhost", "root", "", "health_db");
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MedScan AI | Pneumonia Detection</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #0f172a; --accent: #3b82f6; --success: #10b981; --danger: #ef4444; }
        body { font-family: 'Poppins', sans-serif; background: #f1f5f9; margin: 0; color: #1e293b; padding: 40px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; max-width: 1200px; margin: auto; }
        .card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
        h2 { margin-top: 0; font-size: 1.5rem; display: flex; align-items: center; gap: 10px; }
        
        /* Upload Area */
        .upload-box { border: 2px dashed #cbd5e1; padding: 40px; border-radius: 15px; cursor: pointer; transition: 0.3s; }
        .upload-box:hover { border-color: var(--accent); background: #eff6ff; }
        #imagePreview { width: 100%; border-radius: 10px; margin-top: 15px; display: none; }
        
        .btn { background: var(--accent); color: white; border: none; padding: 12px 24px; border-radius: 10px; font-weight: 600; cursor: pointer; width: 100%; margin-top: 20px; }
        
        /* Table Styling */
        table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
        th { text-align: left; padding: 12px; border-bottom: 2px solid #e2e8f0; color: #64748b; }
        td { padding: 12px; border-bottom: 1px solid #e2e8f0; }
        .badge { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; }
        .bg-NORMAL { background: #d1fae5; color: #065f46; }
        .bg-PNEUMONIA { background: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>

<div class="grid">
    <div class="card">
        <h2>🔍 New Analysis</h2>
        <form action="" method="POST" enctype="multipart/form-data">
            <input type="text" name="patient_name" placeholder="Patient Name" required style="width:100%; padding:10px; margin-bottom:15px; border-radius:8px; border:1px solid #ddd;">
            <div class="upload-box" onclick="document.getElementById('fileInput').click()">
                <p>Click to upload Chest X-Ray</p>
                <input type="file" name="xray" id="fileInput" accept="image/*" hidden onchange="preview(this)">
                <img id="imagePreview">
            </div>
            <button type="submit" name="analyze" class="btn">Generate AI Report</button>
        </form>

        <?php
        if(isset($_POST['analyze'])){
            $p_name = mysqli_real_escape_string($conn, $_POST['patient_name']);
            $target_file = "uploads/" . time() . "_" . basename($_FILES["xray"]["name"]);
            
            if(move_uploaded_file($_FILES["xray"]["tmp_name"], $target_file)){
                $output = shell_exec("python src/predict_logic.py $target_file 2>&1");
                // 1. First, split the output into an array
                $output_parts = explode("\n", trim($output));

                // 2. Then, get the last element of that array variable
                $result_line = end($output_parts);
                
                if(strpos($result_line, '|') !== false){
                    list($label, $prob) = explode("|", $result_line);
                    $conf = $prob * 100;
                    
                    // Save to Database
                    $conn->query("INSERT INTO reports (patient_name, prediction, confidence, image_path) VALUES ('$p_name', '$label', '$conf', '$target_file')");
                    
                    echo "<div style='margin-top:20px; padding:15px; border-radius:10px; background:".($label=='NORMAL'?'#d1fae5':'#fee2e2')."'>";
                    echo "<strong>Result: $label</strong> (".number_format($conf, 1)."% confidence)";
                    echo "</div>";
                }
            }
        }
        ?>
    </div>

    <div class="card">
        <h2>📋 Recent Reports</h2>
        <table>
            <thead>
                <tr>
                    <th>Patient</th>
                    <th>Result</th>
                    <th>Date</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $res = $conn->query("SELECT * FROM reports ORDER BY id DESC LIMIT 5");
                while($row = $res->fetch_assoc()){
                    echo "<tr>
                        <td>{$row['patient_name']}</td>
                        <td><span class='badge bg-{$row['prediction']}'>{$row['prediction']}</span></td>
                        <td>".date('M d, H:i', strtotime($row['created_at']))."</td>
                        <td><a href='generate_report.php?id={$row['id']}' style='text-decoration:none;'>📥 Download</a></td>
                    </tr>";
                }
                ?>
            </tbody>
        </table>
    </div>
</div>

<script>
function preview(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
    }
}
</script>

</body>
</html>