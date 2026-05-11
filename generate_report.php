<?php
require('fpdf.php');

$conn = new mysqli("localhost", "root", "", "health_db");

if(isset($_GET['id'])){

    $id = intval($_GET['id']);
    $res = $conn->query("SELECT * FROM reports WHERE id = $id");

    if(!$res || $res->num_rows == 0){
        die("Report not found");
    }

    $data = $res->fetch_assoc();

    $pdf = new FPDF();
    $pdf->SetAutoPageBreak(false);
    $pdf->AddPage();

    // =========================
    // TITLE
    // =========================
    $pdf->SetFont('Arial','B',16);
    $pdf->Cell(0,10,'MedScan AI Report',0,1,'C');

    // =========================
    // PATIENT INFO
    // =========================
    $pdf->SetFont('Arial','',11);
    $pdf->Cell(0,6,'Patient: '.$data['patient_name'],0,1);
    $pdf->Cell(0,6,'Date: '.$data['created_at'],0,1);
    $pdf->Ln(1);

    // =========================
    // RESULT
    // =========================
    $pdf->SetFont('Arial','B',13);

    if($data['prediction'] == 'NORMAL'){
        $pdf->SetTextColor(0,150,0);
    } else {
        $pdf->SetTextColor(200,0,0);
    }

    $pdf->Cell(0,8,'Prediction: '.$data['prediction'],0,1);

    $pdf->SetTextColor(0,0,0);
    $pdf->SetFont('Arial','',11);
    $pdf->Cell(0,6,'Confidence: '.number_format($data['confidence'],2).'%',0,1);
    $pdf->Ln(2);

    // =========================
    // IMAGE PATHS
    // =========================
    $imagePath = str_replace('/', '\\', __DIR__ . '/' . $data['image_path']);
    $gradcamPath = str_replace('/', '\\', __DIR__ . '/' . $data['gradcam_path']);

    // =========================
    // SIDE BY SIDE IMAGES
    // =========================
    $pdf->SetFont('Arial','B',12);
    $pdf->Cell(0,8,'Analysis Result:',0,1);

    $startY = $pdf->GetY();

    $imgWidth = 85;   // each image width
    $gap = 5;

    // LEFT: Original
    if(file_exists($imagePath)){
        list($w1, $h1) = getimagesize($imagePath);
        $hImg1 = ($h1 / $w1) * $imgWidth;

        $pdf->SetXY(10, $startY);
        $pdf->Cell($imgWidth,6,'Original X-Ray',0,1,'C');

        $pdf->Image($imagePath, 10, $startY + 6, $imgWidth);
    } else {
        $hImg1 = 0;
    }

    // RIGHT: Grad-CAM
    if(file_exists($gradcamPath)){
        list($w2, $h2) = getimagesize($gradcamPath);
        $hImg2 = ($h2 / $w2) * $imgWidth;

        $pdf->SetXY(10 + $imgWidth + $gap, $startY);
        $pdf->Cell($imgWidth,6,'Grad-CAM',0,1,'C');

        $pdf->Image($gradcamPath, 10 + $imgWidth + $gap, $startY + 6, $imgWidth);
    } else {
        $hImg2 = 0;
    }

    // Move cursor below tallest image
    $maxHeight = max($hImg1, $hImg2);
    $pdf->SetY($startY + $maxHeight + 12);

    // =========================
    // INTERPRETATION (IMPORTANT FOR PAPER)
    // =========================
    $pdf->SetFont('Arial','B',12);
    $pdf->Cell(0,8,'AI Heatmap Explanation',0,1);

    $pdf->SetFont('Arial','',11);

    // RED
    $pdf->SetTextColor(220, 20, 60);
    $pdf->Cell(0,7,'[RED / YELLOW] High infection probability regions',0,1);

    // GREEN
    $pdf->SetTextColor(34, 139, 34);
    $pdf->Cell(0,7,'[GREEN] Moderate AI attention regions',0,1);

    // BLUE
    $pdf->SetTextColor(30, 64, 175);
    $pdf->Cell(0,7,'[BLUE] Low or no abnormality detected',0,1);

    // BLACK NORMAL TEXT
    $pdf->SetTextColor(0,0,0);

    $pdf->Ln(3);

    $pdf->MultiCell(
        0,
        5,
        "The Grad-CAM heatmap highlights areas of the chest X-ray that influenced the AI model during prediction. Warmer colors indicate stronger model attention toward potential pneumonia-related patterns."
    );

    // =========================
    // FOOTER
    // =========================
    $pdf->SetY(-12);

    $pdf->SetFont('Arial','I',8);

    $pdf->SetTextColor(120,120,120);

    $pdf->Cell(
        0,
        10,
        'AI-generated report. Not a substitute for medical advice.',
        0,
        0,
        'C'
    );
    // =========================
    // OUTPUT
    // =========================
    $pdf->Output('I', 'Report_'.$data['patient_name'].'.pdf');
}
?>