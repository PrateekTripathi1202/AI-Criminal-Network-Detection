import React, { useState, useEffect, useRef } from 'react';
import { 
  Video, Camera, AlertTriangle, ShieldCheck, Eye, CheckCircle2,
  User, Car, Volume2, VolumeX, Radio, Crosshair, Sparkles, Download, ZoomIn, ZoomOut, Compass, RefreshCw
} from 'lucide-react';
import { soundEffects } from '../services/soundEffects';

// High-definition public surveillance/traffic video streams with procedural fallback
const SURVEILLANCE_SECTORS = [
  {
    camera_id: 'CAM-DEL-041',
    camera_name: 'DELHI CONNAUGHT RADIAL-2 (ANPR PTZ)',
    location: 'Outer Circle Radial-2, Connaught Place, New Delhi',
    lat: '28.6328° N',
    lng: '77.2197° E',
    video_url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
    anpr_target: 'DL-01-AB-9821',
    vehicle_make: 'Toyota Fortuner 4x4 (Black)',
    face_target: "Amit 'Rana' Tyagi",
    face_confidence: 98.4,
    speed: '62 km/h',
    threat: 'CRITICAL',
    fps: '59.94',
    resolution: '3840x2160 4K UHD'
  },
  {
    camera_id: 'CAM-MUM-119',
    camera_name: 'MUMBAI BKC EXPRESSWAY TOLL GATE',
    location: 'Bandra Kurla Complex Connector, Mumbai',
    lat: '19.0657° N',
    lng: '72.8687° E',
    video_url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
    anpr_target: 'MH-04-EK-4402',
    vehicle_make: 'Hyundai Creta (Grey)',
    face_target: "Pooja 'Maya' Deshmukh",
    face_confidence: 94.2,
    speed: '78 km/h',
    threat: 'HIGH',
    fps: '60.00',
    resolution: '1920x1080 FHD'
  },
  {
    camera_id: 'CAM-BLR-088',
    camera_name: 'BENGALURU KORAMANGALA 100FT JUNCTION',
    location: '100 Feet Road, 5th Block Koramangala, Bengaluru',
    lat: '12.9352° N',
    lng: '77.6245° E',
    video_url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
    anpr_target: 'KA-03-MM-1029',
    vehicle_make: 'Maruti Swift (White)',
    face_target: "Sameer 'Sam' Khan",
    face_confidence: 95.8,
    speed: '45 km/h',
    threat: 'HIGH',
    fps: '30.00',
    resolution: '1920x1080 FHD'
  },
  {
    camera_id: 'CAM-HYD-034',
    camera_name: 'HYDERABAD HITEC CITY CYBER GATEWAY',
    location: 'Cyber Towers Junction, Madhapur, Hyderabad',
    lat: '17.4504° N',
    lng: '78.3808° E',
    video_url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyBlazes.mp4',
    anpr_target: 'TS-09-UB-8812',
    vehicle_make: 'Honda City (Silver)',
    face_target: "Karan 'KB' Bansal",
    face_confidence: 91.5,
    speed: '52 km/h',
    threat: 'ELEVATED',
    fps: '48.00',
    resolution: '2560x1440 2K QHD'
  },
  {
    camera_id: 'CAM-KOL-012',
    camera_name: 'KOLKATA VIDYASAGAR SETU TOLL PLAZA',
    location: 'Toll Plaza Approach, Vidyasagar Setu, Kolkata',
    lat: '22.5546° N',
    lng: '88.3242° E',
    video_url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4',
    anpr_target: 'WB-02-AK-9011',
    vehicle_make: 'Mahindra Scorpio (Black)',
    face_target: 'Syndicate Courier Operative',
    face_confidence: 89.2,
    speed: '68 km/h',
    threat: 'MONITORED',
    fps: '60.00',
    resolution: '1920x1080 FHD'
  }
];

export default function CctvSurveillance({ onSelectSuspect }) {
  const [selectedCam, setSelectedCam] = useState(SURVEILLANCE_SECTORS[0]);
  const [visionMode, setVisionMode] = useState('OPTICAL'); // 'OPTICAL' | 'NIGHT_VISION' | 'THERMAL' | 'WIREFRAME'
  const [isWebcamActive, setIsWebcamActive] = useState(false);
  const [webcamError, setWebcamError] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [audioFeedback, setAudioFeedback] = useState(true);
  const [videoFailed, setVideoFailed] = useState(false);
  const [snapshotTaken, setSnapshotTaken] = useState(false);
  const [feedMode, setFeedMode] = useState('STREAM'); // 'STREAM' | 'PROCEDURAL'

  const videoRef = useRef(null);
  const webcamVideoRef = useRef(null);
  const overlayCanvasRef = useRef(null);
  const proceduralCanvasRef = useRef(null);
  const streamRef = useRef(null);

  // Toggle Laptop/Device Webcam
  const toggleWebcam = async () => {
    soundEffects.playClick();
    if (isWebcamActive) {
      stopWebcam();
    } else {
      startWebcam();
    }
  };

  const startWebcam = async () => {
    setWebcamError(null);
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Webcam media API not supported in this browser.');
      }
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
          audio: false
        });
      } catch (constraintErr) {
        console.warn('Ideal constraints failed, attempting fallback to basic video stream:', constraintErr);
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      }

      streamRef.current = stream;
      if (webcamVideoRef.current) {
        webcamVideoRef.current.srcObject = stream;
        try {
          await webcamVideoRef.current.play();
        } catch (playErr) {
          console.warn('Webcam autoplay warning:', playErr);
        }
      }
      setIsWebcamActive(true);
      if (audioFeedback) soundEffects.playTargetLock();
    } catch (err) {
      console.error('Webcam access error:', err);
      setWebcamError(err.message || 'Permission denied or webcam busy.');
      setIsWebcamActive(false);
    }
  };

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (webcamVideoRef.current) {
      webcamVideoRef.current.srcObject = null;
    }
    setIsWebcamActive(false);
  };

  // Clean up stream on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
      }
    };
  }, []);

  // When webcamVideoRef mounts or stream changes, ensure srcObject is bound
  useEffect(() => {
    if (isWebcamActive && streamRef.current && webcamVideoRef.current) {
      if (webcamVideoRef.current.srcObject !== streamRef.current) {
        webcamVideoRef.current.srcObject = streamRef.current;
        webcamVideoRef.current.play().catch(() => {});
      }
    }
  }, [isWebcamActive]);

  // Handle external video error -> activate procedural visualizer
  const handleVideoError = () => {
    console.warn(`[CCTV] Stream ${selectedCam.camera_id} video element triggered fallback.`);
    setVideoFailed(true);
  };

  // Procedural Simulated Video Generator (Active if MP4 fails or user toggles)
  useEffect(() => {
    const canvas = proceduralCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animId;
    let tick = 0;

    const cars = [
      { x: 100, y: 220, speed: 2.8, color: '#f59e0b', plate: selectedCam.anpr_target },
      { x: 400, y: 290, speed: 3.5, color: '#0ea5e9', plate: 'DL-03-CX-4102' },
      { x: 600, y: 350, speed: 2.2, color: '#ef4444', plate: 'HR-26-DJ-9099' }
    ];

    const renderProcedural = () => {
      tick++;
      const w = canvas.width;
      const h = canvas.height;

      // Dark Asphalt Highway Background
      ctx.fillStyle = '#080d1a';
      ctx.fillRect(0, 0, w, h);

      // Perspective Road Horizon
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.moveTo(w * 0.35, h * 0.3);
      ctx.lineTo(w * 0.65, h * 0.3);
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fill();

      // Road Lane Markings
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
      ctx.lineWidth = 3;
      ctx.setLineDash([20, 15]);
      ctx.lineDashOffset = -tick * 4;

      ctx.beginPath();
      ctx.moveTo(w * 0.5, h * 0.3);
      ctx.lineTo(w * 0.35, h);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(w * 0.5, h * 0.3);
      ctx.lineTo(w * 0.65, h);
      ctx.stroke();
      ctx.setLineDash([]);

      // Overhead Gantry structure
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 4;
      ctx.strokeRect(w * 0.15, h * 0.2, w * 0.7, 10);

      // Render Moving Vehicles
      cars.forEach((car) => {
        car.x = (car.x + car.speed) % (w + 120);
        const drawX = car.x - 60;

        // Vehicle body
        ctx.fillStyle = car.color;
        ctx.fillRect(drawX, car.y, 110, 50);

        // Headlights glow
        ctx.fillStyle = 'rgba(254, 240, 138, 0.35)';
        ctx.beginPath();
        ctx.moveTo(drawX + 110, car.y + 10);
        ctx.lineTo(drawX + 220, car.y - 15);
        ctx.lineTo(drawX + 220, car.y + 65);
        ctx.closePath();
        ctx.fill();

        // Wheels
        ctx.fillStyle = '#020617';
        ctx.fillRect(drawX + 15, car.y + 45, 25, 12);
        ctx.fillRect(drawX + 70, car.y + 45, 25, 12);
      });

      animId = requestAnimationFrame(renderProcedural);
    };

    renderProcedural();
    return () => cancelAnimationFrame(animId);
  }, [selectedCam, videoFailed, feedMode]);

  // Real-time Canvas AI Computer Vision Tracker Overlay
  useEffect(() => {
    const canvas = overlayCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animId;
    let frame = 0;

    const drawBracket = (x, y, bw, bh, col = '#ff0055') => {
      ctx.strokeStyle = col;
      ctx.lineWidth = 2.5;
      const len = 16;
      // Top Left
      ctx.beginPath(); ctx.moveTo(x, y + len); ctx.lineTo(x, y); ctx.lineTo(x + len, y); ctx.stroke();
      // Top Right
      ctx.beginPath(); ctx.moveTo(x + bw - len, y); ctx.lineTo(x + bw, y); ctx.lineTo(x + bw, y + len); ctx.stroke();
      // Bottom Left
      ctx.beginPath(); ctx.moveTo(x, y + bh - len); ctx.lineTo(x, y + bh); ctx.lineTo(x + len, y + bh); ctx.stroke();
      // Bottom Right
      ctx.beginPath(); ctx.moveTo(x + bw - len, y + bh); ctx.lineTo(x + bw, y + bh); ctx.lineTo(x + bw, y + bh - len); ctx.stroke();
    };

    const renderOverlay = () => {
      frame++;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const w = canvas.width;
      const h = canvas.height;

      // 1. Vision Mode Shaders
      if (visionMode === 'NIGHT_VISION') {
        ctx.fillStyle = 'rgba(16, 185, 129, 0.12)';
        ctx.fillRect(0, 0, w, h);
      } else if (visionMode === 'THERMAL') {
        ctx.fillStyle = 'rgba(239, 68, 68, 0.10)';
        ctx.fillRect(0, 0, w, h);
      } else if (visionMode === 'WIREFRAME') {
        ctx.fillStyle = 'rgba(6, 182, 212, 0.08)';
        ctx.fillRect(0, 0, w, h);
      }

      if (!isWebcamActive) {
        // CCTV Simulated Detections
        const vX = 140 + Math.sin(frame * 0.02) * 35;
        const vY = 170 + Math.cos(frame * 0.015) * 12;
        const vW = 320;
        const vH = 180;

        // Vehicle Tracking Box
        drawBracket(vX, vY, vW, vH, '#f59e0b');
        ctx.fillStyle = 'rgba(245, 158, 11, 0.95)';
        ctx.fillRect(vX, vY - 26, 260, 24);
        ctx.fillStyle = '#050b14';
        ctx.font = 'bold 11px JetBrains Mono, monospace';
        ctx.fillText(`ANPR: ${selectedCam.anpr_target} | ${selectedCam.speed}`, vX + 6, vY - 10);

        // Vehicle Make pill
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.fillRect(vX, vY + vH + 4, 260, 20);
        ctx.fillStyle = '#f8fafc';
        ctx.font = '10px Inter, sans-serif';
        ctx.fillText(`VEHICLE: ${selectedCam.vehicle_make}`, vX + 6, vY + vH + 18);

        // Face Tracking Box inside vehicle / nearby
        const fX = vX + 50;
        const fY = vY + 30;
        const fW = 95;
        const fH = 95;
        drawBracket(fX, fY, fW, fH, '#ef4444');

        ctx.fillStyle = 'rgba(239, 68, 68, 0.95)';
        ctx.fillRect(fX, fY - 24, 200, 22);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 11px JetBrains Mono, monospace';
        ctx.fillText(`MATCH: ${selectedCam.face_target}`, fX + 6, fY - 9);

        // Biometric Confidence meter
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.fillRect(fX, fY + fH + 4, 200, 20);
        ctx.fillStyle = '#00f2fe';
        ctx.font = 'bold 10px JetBrains Mono, monospace';
        ctx.fillText(`CCTNS BIO-MATCH: ${selectedCam.face_confidence}%`, fX + 6, fY + fH + 18);

      } else {
        // REAL DEVICE WEBCAM OPERATOR HUD
        const cX = w / 2 - 110;
        const cY = h / 2 - 120;
        const cW = 220;
        const cH = 240;

        drawBracket(cX, cY, cW, cH, '#10b981');

        // Dynamic Facial Scanning Reticle
        const scanY = cY + (Math.sin(frame * 0.05) * 0.5 + 0.5) * cH;
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.8)';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(cX, scanY);
        ctx.lineTo(cX + cW, scanY);
        ctx.stroke();

        // Top Auth Badge
        ctx.fillStyle = 'rgba(16, 185, 129, 0.95)';
        ctx.fillRect(cX, cY - 28, 280, 26);
        ctx.fillStyle = '#050b14';
        ctx.font = 'bold 11px JetBrains Mono, monospace';
        ctx.fillText('LE OPERATOR DETECTED: AUTH #DL-4902', cX + 6, cY - 11);

        // Bottom Bio Particulars
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.fillRect(cX, cY + cH + 6, 280, 24);
        ctx.fillStyle = '#34d399';
        ctx.font = '10px JetBrains Mono, monospace';
        ctx.fillText('CLEARANCE: LEVEL 5 (DIRECTORATE APPROVED)', cX + 6, cY + cH + 22);
      }

      // Center Crosshair
      ctx.strokeStyle = 'rgba(56, 189, 248, 0.4)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(w / 2 - 20, h / 2); ctx.lineTo(w / 2 + 20, h / 2);
      ctx.moveTo(w / 2, h / 2 - 20); ctx.lineTo(w / 2, h / 2 + 20);
      ctx.stroke();

      // Top OSD Metadata
      ctx.fillStyle = '#00f2fe';
      ctx.font = '11px JetBrains Mono, monospace';
      ctx.fillText(`SYS: NCIS OPTICAL GRID [${selectedCam.camera_id}] • ZOOM: ${zoomLevel}x`, 16, 26);
      ctx.fillText(`GEO: ${selectedCam.lat}, ${selectedCam.lng} | ${selectedCam.fps} FPS`, 16, 44);

      // Blinking REC Indicator
      if (Math.floor(frame / 25) % 2 === 0) {
        ctx.fillStyle = '#ef4444';
        ctx.beginPath(); ctx.arc(w - 24, 22, 6, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 10px Inter, sans-serif';
        ctx.fillText('LIVE RECORD', w - 105, 26);
      }

      animId = requestAnimationFrame(renderOverlay);
    };

    renderOverlay();
    return () => cancelAnimationFrame(animId);
  }, [selectedCam, visionMode, isWebcamActive, zoomLevel]);

  // Capture Snapshot of Current Stream
  const captureSnapshot = () => {
    soundEffects.playSnapshot();
    setSnapshotTaken(true);
    setTimeout(() => setSnapshotTaken(false), 1200);

    const canvas = document.createElement('canvas');
    canvas.width = 1280;
    canvas.height = 720;
    const ctx = canvas.getContext('2d');

    // Draw video or procedural
    if (isWebcamActive && webcamVideoRef.current) {
      ctx.drawImage(webcamVideoRef.current, 0, 0, 1280, 720);
    } else if (videoRef.current && !videoFailed && feedMode === 'STREAM') {
      ctx.drawImage(videoRef.current, 0, 0, 1280, 720);
    } else if (proceduralCanvasRef.current) {
      ctx.drawImage(proceduralCanvasRef.current, 0, 0, 1280, 720);
    }

    // Add forensic watermark
    ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
    ctx.fillRect(0, 660, 1280, 60);
    ctx.fillStyle = '#00f2fe';
    ctx.font = 'bold 18px monospace';
    const stamp = new Date().toISOString() + ` | CCTNS FORENSIC RECORD | CAM: ${selectedCam.camera_id}`;
    ctx.fillText(stamp, 24, 698);

    // Trigger download
    const a = document.createElement('a');
    a.download = `SURVEILLANCE_${selectedCam.camera_id}_${Date.now()}.png`;
    a.href = canvas.toDataURL('image/png');
    a.click();
  };

  const isShowingProcedural = videoFailed || feedMode === 'PROCEDURAL';

  return (
    <div className="space-y-4">
      {/* Top Surveillance Control Bar */}
      <div className="glass-panel p-4 flex flex-wrap items-center justify-between gap-3 border-l-4 border-rose-500">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-rose-950/80 border border-rose-500/40 flex items-center justify-center text-rose-400">
            <Video className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-display font-bold text-sm tracking-wide text-slate-100">
                REAL CCTV SURVEILLANCE & BIOMETRIC RECOGNITION (4K UHD)
              </h2>
              <span className="badge badge-critical text-[10px]">CCTNS LIVE FEED</span>
            </div>
            <p className="text-xs text-slate-400">
              Multi-Camera PTZ Stream • YOLOv11 Multi-Object Detection • DeepFace Biometric Matching
            </p>
          </div>
        </div>

        {/* Tactical Vision Mode Selectors */}
        <div className="flex items-center gap-2 flex-wrap">
          <div className="flex items-center bg-slate-900/90 rounded-lg p-1 border border-slate-700/60 text-xs">
            <button
              onClick={() => { soundEffects.playClick(); setVisionMode('OPTICAL'); }}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                visionMode === 'OPTICAL' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Optical HD
            </button>
            <button
              onClick={() => { soundEffects.playClick(); setVisionMode('NIGHT_VISION'); }}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                visionMode === 'NIGHT_VISION' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Night-Vision IR
            </button>
            <button
              onClick={() => { soundEffects.playClick(); setVisionMode('THERMAL'); }}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                visionMode === 'THERMAL' ? 'bg-rose-500 text-white font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Thermal FLIR
            </button>
            <button
              onClick={() => { soundEffects.playClick(); setVisionMode('WIREFRAME'); }}
              className={`px-3 py-1 rounded-md font-medium transition-all ${
                visionMode === 'WIREFRAME' ? 'bg-cyan-400 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Wireframe Edge
            </button>
          </div>

          {/* Device Webcam Toggle Button */}
          <button
            onClick={toggleWebcam}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all shadow-md ${
              isWebcamActive
                ? 'bg-rose-600 text-white shadow-rose-600/30 animate-pulse'
                : 'bg-emerald-600 hover:bg-emerald-500 text-slate-950 shadow-emerald-500/30'
            }`}
          >
            <Camera className="w-3.5 h-3.5" />
            {isWebcamActive ? 'Disconnect Device Webcam' : 'Enable My Device Webcam'}
          </button>
        </div>
      </div>

      {webcamError && (
        <div className="bg-rose-950/60 border border-rose-500/40 p-3 rounded-lg text-rose-300 text-xs flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            <span>Webcam Access Error: {webcamError}. Ensure camera permissions are allowed in your browser.</span>
          </div>
          <button onClick={() => setWebcamError(null)} className="text-slate-400 hover:text-white">✕</button>
        </div>
      )}

      {/* Main Video View & Target Inspection Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Real Video Player Container with Canvas Overlay */}
        <div className="lg:col-span-8 glass-panel p-3 relative scanline-overlay overflow-hidden">
          <div className="relative w-full h-[470px] bg-black rounded-lg overflow-hidden border border-slate-700/60">
            {/* 1. CCTV Video Stream */}
            <video
              ref={videoRef}
              src={selectedCam.video_url}
              autoPlay
              loop
              muted
              playsInline
              onError={handleVideoError}
              style={{
                position: 'absolute',
                inset: 0,
                opacity: !isWebcamActive && !isShowingProcedural ? 1 : 0,
                pointerEvents: !isWebcamActive && !isShowingProcedural ? 'auto' : 'none',
                zIndex: !isWebcamActive && !isShowingProcedural ? 2 : 0,
                transform: `scale(${zoomLevel})`,
                transformOrigin: 'center center',
                transition: 'transform 0.3s ease, opacity 0.2s ease'
              }}
              className={`w-full h-full object-cover ${
                visionMode === 'NIGHT_VISION' ? 'filter saturate-200 brightness-125 contrast-150 hue-rotate-90' : ''
              } ${
                visionMode === 'THERMAL' ? 'filter invert contrast-200 hue-rotate-180' : ''
              } ${
                visionMode === 'WIREFRAME' ? 'filter contrast-200 grayscale' : ''
              }`}
            />

            {/* 2. Procedural Fallback Canvas (Active if MP4 fails, offline, or toggled) */}
            <canvas
              ref={proceduralCanvasRef}
              width={760}
              height={470}
              style={{
                position: 'absolute',
                inset: 0,
                opacity: !isWebcamActive && isShowingProcedural ? 1 : 0,
                pointerEvents: !isWebcamActive && isShowingProcedural ? 'auto' : 'none',
                zIndex: !isWebcamActive && isShowingProcedural ? 2 : 0,
                transform: `scale(${zoomLevel})`,
                transformOrigin: 'center center',
                transition: 'transform 0.3s ease, opacity 0.2s ease'
              }}
              className="w-full h-full object-cover"
            />

            {/* 3. Real Device Webcam Video Element (Always in layout tree, fully active) */}
            <video
              ref={webcamVideoRef}
              autoPlay
              playsInline
              muted
              style={{
                position: 'absolute',
                inset: 0,
                opacity: isWebcamActive ? 1 : 0,
                pointerEvents: isWebcamActive ? 'auto' : 'none',
                zIndex: isWebcamActive ? 5 : 0,
                transform: `scaleX(-1) scale(${zoomLevel})`,
                transformOrigin: 'center center',
                transition: 'transform 0.3s ease, opacity 0.2s ease'
              }}
              className={`w-full h-full object-cover ${
                visionMode === 'NIGHT_VISION' ? 'filter saturate-200 brightness-125 contrast-150 hue-rotate-90' : ''
              } ${
                visionMode === 'THERMAL' ? 'filter invert contrast-200 hue-rotate-180' : ''
              }`}
            />

            {/* Canvas overlay directly on top of video */}
            <canvas
              ref={overlayCanvasRef}
              width={760}
              height={470}
              style={{ zIndex: 10 }}
              className="absolute inset-0 w-full h-full pointer-events-none"
            />

            {/* Snapshot Flash Feedback */}
            {snapshotTaken && (
              <div className="absolute inset-0 bg-white/40 pointer-events-none animate-pulse transition-opacity z-20" />
            )}

            {/* PTZ Zoom & Camera Action Floating Bar */}
            <div className="absolute bottom-3 right-3 flex items-center gap-1.5 bg-slate-950/85 backdrop-blur-md p-1.5 rounded-lg border border-slate-700/60 z-20">
              <button
                onClick={() => { soundEffects.playClick(); setZoomLevel(prev => Math.max(1, prev - 0.5)); }}
                className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-800 rounded transition-all"
                title="Zoom Out"
              >
                <ZoomOut className="w-4 h-4" />
              </button>
              <span className="text-[11px] font-mono text-cyan-400 font-bold px-1.5">{zoomLevel}x</span>
              <button
                onClick={() => { soundEffects.playClick(); setZoomLevel(prev => Math.min(3, prev + 0.5)); }}
                className="p-1.5 text-slate-300 hover:text-white hover:bg-slate-800 rounded transition-all"
                title="Zoom In"
              >
                <ZoomIn className="w-4 h-4" />
              </button>
              <div className="h-4 w-[1px] bg-slate-700 mx-1" />
              <button
                onClick={captureSnapshot}
                className="px-2 py-1 bg-cyan-600 hover:bg-cyan-500 text-slate-950 text-[11px] font-bold rounded flex items-center gap-1 transition-all"
                title="Save Forensic Snapshot"
              >
                <Download className="w-3.5 h-3.5" />
                Snapshot
              </button>
            </div>
          </div>

          {/* Under-video Camera Switcher Strip */}
          <div className="flex items-center justify-between mt-3 px-1 text-xs flex-wrap gap-2">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-slate-400 font-semibold flex items-center gap-1">
                <Compass className="w-3.5 h-3.5 text-cyan-400" />
                Sectors:
              </span>
              {SURVEILLANCE_SECTORS.map(cam => (
                <button
                  key={cam.camera_id}
                  onClick={() => {
                    soundEffects.playClick();
                    setSelectedCam(cam);
                    setVideoFailed(false);
                    setIsWebcamActive(false);
                  }}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                    selectedCam.camera_id === cam.camera_id && !isWebcamActive
                      ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/50 shadow-sm'
                      : 'bg-slate-800/60 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {cam.camera_id} • {cam.location.split(',')[1]?.trim() || cam.camera_name.split(' ')[0]}
                </button>
              ))}
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  soundEffects.playClick();
                  setFeedMode(feedMode === 'STREAM' ? 'PROCEDURAL' : 'STREAM');
                }}
                className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded text-xs font-mono border border-cyan-500/30"
                title="Toggle between Cloud Video Stream and Procedural Tactical Radar"
              >
                Feed: {feedMode === 'STREAM' ? 'Optical 4K' : 'Radar Sim'}
              </button>

              <button
                onClick={() => setAudioFeedback(!audioFeedback)}
                className={`p-1.5 rounded-lg border text-xs flex items-center gap-1 transition-all ${
                  audioFeedback
                    ? 'border-cyan-500/40 text-cyan-400 bg-cyan-950/30'
                    : 'border-slate-700 text-slate-500'
                }`}
                title="Toggle Radar Lock Audio Chime"
              >
                {audioFeedback ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5" />}
                Radar Audio
              </button>
            </div>
          </div>
        </div>

        {/* Right Inspection & Telemetry Panel */}
        <div className="lg:col-span-4 space-y-4">
          {/* Target Detection Card */}
          <div className="glass-panel p-4 space-y-3 border-t-4 border-amber-500">
            <div className="flex items-center justify-between">
              <h3 className="font-display font-bold text-xs tracking-wider text-slate-200 flex items-center gap-1.5">
                <Crosshair className="w-4 h-4 text-amber-400" />
                ACTIVE TARGET TELEMETRY
              </h3>
              <span className={`badge ${selectedCam.threat === 'CRITICAL' ? 'badge-critical' : 'badge-high'} text-[10px]`}>
                {selectedCam.threat}
              </span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                <div className="flex justify-between text-slate-400">
                  <span>ANPR License Plate:</span>
                  <span className="font-mono font-bold text-amber-400">{selectedCam.anpr_target}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Vehicle Model:</span>
                  <span className="text-slate-200 font-medium">{selectedCam.vehicle_make}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Tracked Speed:</span>
                  <span className="font-mono text-cyan-300 font-semibold">{selectedCam.speed}</span>
                </div>
              </div>

              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                <div className="flex justify-between text-slate-400">
                  <span>Suspect Facial Match:</span>
                  <span className="font-bold text-rose-400">{selectedCam.face_target}</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Neural Biometric Score:</span>
                  <span className="font-mono font-bold text-cyan-300">{selectedCam.face_confidence}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2 mt-1 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-cyan-500 to-rose-500 h-2 rounded-full transition-all duration-500" 
                    style={{ width: `${selectedCam.face_confidence}%` }}
                  />
                </div>
              </div>
            </div>

            <button
              onClick={() => onSelectSuspect && onSelectSuspect(selectedCam.face_target)}
              className="w-full py-2 bg-gradient-to-r from-rose-600 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-slate-950 font-bold text-xs rounded-lg flex items-center justify-center gap-1.5 transition-all shadow-md"
            >
              <Eye className="w-3.5 h-3.5" />
              Trace Suspect in 3D Knowledge Graph
            </button>
          </div>

          {/* Live Incident Sightings Log */}
          <div className="glass-panel p-4 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-display font-bold text-xs tracking-wider text-slate-200">
                RECENT ANPR & BIOMETRIC HITS
              </h3>
              <span className="text-[10px] text-cyan-400 font-mono">3 SIGHTINGS</span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div className="space-y-0.5">
                  <div className="font-bold text-slate-200">DL-01-AB-9821</div>
                  <div className="text-[10px] text-slate-400">Delhi Radial-2 • VEHICLE</div>
                </div>
                <div className="text-right">
                  <span className="badge badge-critical text-[9px]">CRITICAL</span>
                  <div className="text-[10px] font-mono text-slate-500 mt-0.5">22:42:10</div>
                </div>
              </div>
              <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div className="space-y-0.5">
                  <div className="font-bold text-slate-200">Amit 'Rana' Tyagi</div>
                  <div className="text-[10px] text-slate-400">Delhi Radial-2 • BIOMETRIC</div>
                </div>
                <div className="text-right">
                  <span className="badge badge-critical text-[9px]">CRITICAL</span>
                  <div className="text-[10px] font-mono text-slate-500 mt-0.5">22:41:45</div>
                </div>
              </div>
              <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                <div className="space-y-0.5">
                  <div className="font-bold text-slate-200">MH-04-EK-4402</div>
                  <div className="text-[10px] text-slate-400">Mumbai BKC Toll • VEHICLE</div>
                </div>
                <div className="text-right">
                  <span className="badge badge-critical text-[9px]">HIGH</span>
                  <div className="text-[10px] font-mono text-slate-500 mt-0.5">22:40:12</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
