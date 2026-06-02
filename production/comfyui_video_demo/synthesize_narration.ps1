param(
    [string]$Root = "F:\CodexSharedCockpit\production\comfyui_video_demo"
)

Add-Type -AssemblyName System.Speech
$voiceName = "Microsoft Huihui Desktop"
$segmentsPath = Join-Path $Root "narration_segments.txt"
$outDir = Join-Path $Root "audio"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice($voiceName)
$synth.Rate = -1
$synth.Volume = 100

Get-Content -LiteralPath $segmentsPath -Encoding UTF8 | ForEach-Object {
    if ($_ -notmatch "\|") { return }
    $parts = $_.Split("|", 2)
    $id = $parts[0]
    $text = $parts[1]
    $wav = Join-Path $outDir ("segment_" + $id + ".wav")
    $synth.SetOutputToWaveFile($wav)
    $synth.Speak($text)
    $synth.SetOutputToNull()
    Write-Output $wav
}
