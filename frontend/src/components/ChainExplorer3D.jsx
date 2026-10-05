import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { User, Phone, Car, CreditCard, MapPin, Video, ArrowRight, CheckCircle2, ShieldCheck, Sparkles } from 'lucide-react';

const CHAIN_STAGES = [
  {
    step: 1,
    key: 'person',
    title: '1. Suspect Entity (Person)',
    icon: User,
    colorHex: 0xff0055,
    name: "Rajesh 'Munna' Sharma",
    type: "Hawala Logistics Lieutenant",
    evidence: "CCTNS Wanted ID CCTNS-2025-DL-4102. Identified via intercepted audio recordings commanding extortion payoffs.",
    confidence: "98.4%",
    badge: "CRITICAL SUSPECT"
  },
  {
    step: 2,
    key: 'phone',
    title: '2. Burner Device (Phone)',
    icon: Phone,
    colorHex: 0x00f2fe,
    name: "+91 98110-XXXX1 (Burner SIM)",
    type: "Telecom Trace & IMEI Match",
    evidence: "Tower triangulation matches Sharma's safehouse. 78 late-night encrypted calls to Kingpin Vicky Malhotra's satellite VoIP.",
    confidence: "99.1%",
    badge: "COMMUNICATION LINK"
  },
  {
    step: 3,
    key: 'vehicle',
    title: '3. Transport Asset (Vehicle)',
    icon: Car,
    colorHex: 0xf59e0b,
    name: "DL-01-AB-9821 (Black Fortuner)",
    type: "ANPR Sighting & Infotainment Dump",
    evidence: "Vehicle infotainment Bluetooth paired with Burner SIM IMEI. Sighted fleeing crime scene at 21:14 PM.",
    confidence: "97.6%",
    badge: "GETAWAY ASSET"
  },
  {
    step: 4,
    key: 'account',
    title: '4. Financial Funnel (Account)',
    icon: CreditCard,
    colorHex: 0x10b981,
    name: "HDFC #...8819 (Apex Impex)",
    type: "Hawala Layering Node",
    evidence: "Extortion ransom transferred from ICICI account into this corporate shell entity to purchase the Fortuner SUV.",
    confidence: "95.8%",
    badge: "MONEY TRAIL"
  },
  {
    step: 5,
    key: 'location',
    title: '5. Crime Hotspot (Location)',
    icon: MapPin,
    colorHex: 0xec4899,
    name: "Connaught Place Block-B, Delhi",
    type: "Incident & Handover Scene",
    evidence: "Geofence boundary breach triggered. Suspect vehicle remained parked in service alley for 45 minutes.",
    confidence: "99.0%",
    badge: "CRIME SCENE"
  },
  {
    step: 6,
    key: 'cctv',
    title: '6. Biometric Confirmation (CCTV)',
    icon: Video,
    colorHex: 0x06b6d4,
    name: "CCTV #DEL-CP-041 (4K PTZ)",
    type: "AI Facial & ANPR Match",
    evidence: "Facial recognition AI verified hitman Amit 'Rana' Tyagi exiting vehicle with 94.8% confidence match.",
    confidence: "94.8%",
    badge: "EVIDENTIARY PROOF"
  }
];

export default function ChainExplorer3D() {
  const mountRef = useRef(null);
  const [activeStep, setActiveStep] = useState(1);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const stagesMeshesRef = useRef([]);

  useEffect(() => {
    if (!mountRef.current) return;
    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = new THREE.Color(0x060913);

    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(0, 30, 220);
    cameraRef.current = camera;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    mountRef.current.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.9);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0x00f2fe, 1.5);
    dirLight.position.set(100, 100, 100);
    scene.add(dirLight);

    // Grid Floor
    const grid = new THREE.GridHelper(350, 20, 0x1e293b, 0x0f172a);
    grid.position.y = -35;
    scene.add(grid);

    // Stage positions along an S-curve or straight line
    stagesMeshesRef.current = [];
    const stepSpacing = 50;
    const startX = -((CHAIN_STAGES.length - 1) * stepSpacing) / 2;

    const points = [];

    CHAIN_STAGES.forEach((stage, idx) => {
      const x = startX + idx * stepSpacing;
      const y = Math.sin(idx * 0.8) * 12;
      const z = Math.cos(idx * 0.8) * 20;
      points.push(new THREE.Vector3(x, y, z));

      const stageGroup = new THREE.Group();
      stageGroup.position.set(x, y, z);

      // 3D Solid Geometry
      let geom;
      if (stage.key === 'person') geom = new THREE.SphereGeometry(9, 24, 24);
      else if (stage.key === 'phone') geom = new THREE.CylinderGeometry(5, 5, 14, 16);
      else if (stage.key === 'vehicle') geom = new THREE.BoxGeometry(16, 9, 11);
      else if (stage.key === 'account') geom = new THREE.CylinderGeometry(9, 9, 4, 16);
      else if (stage.key === 'location') geom = new THREE.ConeGeometry(8, 16, 16);
      else geom = new THREE.TorusGeometry(8, 2.5, 16, 32);

      const mat = new THREE.MeshStandardMaterial({
        color: stage.colorHex,
        roughness: 0.2,
        metalness: 0.8,
        emissive: stage.colorHex,
        emissiveIntensity: 0.4
      });

      const mesh = new THREE.Mesh(geom, mat);
      stageGroup.add(mesh);

      // Surrounding Orbit Ring
      const ringGeom = new THREE.RingGeometry(14, 15.5, 32);
      const ringMat = new THREE.MeshBasicMaterial({
        color: stage.colorHex,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.6
      });
      const ring = new THREE.Mesh(ringGeom, ringMat);
      ring.name = 'ring';
      stageGroup.add(ring);

      scene.add(stageGroup);
      stagesMeshesRef.current.push({ group: stageGroup, step: stage.step, colorHex: stage.colorHex, pos: new THREE.Vector3(x, y, z) });
    });

    // Connecting laser conduit line
    const curve = new THREE.CatmullRomCurve3(points);
    const lineGeom = new THREE.BufferGeometry().setFromPoints(curve.getPoints(60));
    const lineMat = new THREE.LineBasicMaterial({ color: 0x00f2fe, transparent: true, opacity: 0.75, linewidth: 2 });
    const line = new THREE.Line(lineGeom, lineMat);
    scene.add(line);

    // Particle pulse along line
    const particleGeom = new THREE.SphereGeometry(2.5, 12, 12);
    const particleMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const particle = new THREE.Mesh(particleGeom, particleMat);
    scene.add(particle);

    let animId;
    let clock = new THREE.Clock();

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const t = clock.getElapsedTime();

      // Move particle along curve
      const pT = (t * 0.2) % 1.0;
      particle.position.copy(curve.getPointAt(pT));

      // Rotate stage rings
      stagesMeshesRef.current.forEach(item => {
        const ring = item.group.getObjectByName('ring');
        if (ring) ring.rotation.z += 0.02;
        if (ring) ring.rotation.x = Math.sin(t * 2) * 0.2;
      });

      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(animId);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  // Animate camera to focus on selected step
  useEffect(() => {
    if (!cameraRef.current || !stagesMeshesRef.current.length) return;
    const targetStage = stagesMeshesRef.current.find(s => s.step === activeStep);
    if (targetStage) {
      const pos = targetStage.pos;
      cameraRef.current.position.x = pos.x;
      cameraRef.current.position.y = pos.y + 15;
      cameraRef.current.position.z = pos.z + 120;
      cameraRef.current.lookAt(pos.x, pos.y, pos.z);
    }
  }, [activeStep]);

  const currentStageData = CHAIN_STAGES.find(s => s.step === activeStep) || CHAIN_STAGES[0];
  const IconComponent = currentStageData.icon;

  return (
    <div className="space-y-4">
      {/* PPT Relationship Chain Header Banner */}
      <div className="glass-panel p-4 flex flex-wrap items-center justify-between gap-3 border-l-4 border-cyan-400">
        <div>
          <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest">
            RELATIONAL FORENSIC CHAIN RECONSTRUCTION // CCTNS STANDARD
          </span>
          <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            MULTI-LAYERED CRIMINAL CONDUIT: Person ➔ Phone ➔ Vehicle ➔ Account ➔ Location ➔ CCTV
          </h2>
        </div>
        <div className="flex items-center gap-1.5 overflow-x-auto text-xs">
          {CHAIN_STAGES.map(stage => (
            <button
              key={stage.step}
              onClick={() => setActiveStep(stage.step)}
              className={`px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all font-medium ${
                activeStep === stage.step
                  ? 'bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20'
                  : 'bg-slate-800/60 text-slate-300 hover:bg-slate-700/60'
              }`}
            >
              <span>{stage.step}.</span> {stage.key.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* 3D Visualizer & Detail Stage */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-7 relative h-[440px] rounded-xl overflow-hidden glass-panel border border-cyan-500/20">
          <div ref={mountRef} className="w-full h-full" />
          <div className="absolute bottom-3 left-3 p-2.5 glass-panel text-[11px] text-slate-300 pointer-events-auto">
            Stage {activeStep} of 6 in 3D Perspective. Click below to walk through evidence chain.
          </div>
        </div>

        {/* Stage Evidentiary Dossier Card */}
        <div className="lg:col-span-5 glass-panel p-5 flex flex-col justify-between space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="badge badge-cyber">{currentStageData.badge}</span>
              <span className="text-xs text-cyan-400 font-mono font-semibold">AI Confidence: {currentStageData.confidence}</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-3 rounded-xl bg-slate-900 border border-slate-700/60 text-cyan-400">
                <IconComponent className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-display font-bold text-lg text-slate-100">{currentStageData.name}</h3>
                <p className="text-xs text-slate-400">{currentStageData.type}</p>
              </div>
            </div>

            <div className="p-3.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed">
              <div className="font-semibold text-slate-200 mb-1 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" /> Forensic Link Verification:
              </div>
              {currentStageData.evidence}
            </div>

            {/* Complete chain progression dots */}
            <div className="pt-2">
              <span className="text-[11px] text-slate-400 font-medium block mb-2">Relational Chain Flow:</span>
              <div className="flex items-center gap-2 text-xs">
                {CHAIN_STAGES.map((s, idx) => (
                  <React.Fragment key={s.step}>
                    <button
                      onClick={() => setActiveStep(s.step)}
                      className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs transition-all ${
                        activeStep === s.step
                          ? 'bg-cyan-400 text-slate-950 scale-110 shadow-sm shadow-cyan-400/50'
                          : (s.step < activeStep ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40' : 'bg-slate-800 text-slate-400')
                      }`}
                    >
                      {s.step}
                    </button>
                    {idx < CHAIN_STAGES.length - 1 && <span className="text-slate-600 font-bold">➔</span>}
                  </React.Fragment>
                ))}
              </div>
            </div>
          </div>

          {/* Stepper Buttons */}
          <div className="flex items-center justify-between pt-3 border-t border-slate-800">
            <button
              onClick={() => setActiveStep(prev => Math.max(1, prev - 1))}
              disabled={activeStep === 1}
              className="btn-secondary text-xs disabled:opacity-40"
            >
              Previous Link
            </button>
            <button
              onClick={() => setActiveStep(prev => Math.min(6, prev + 1))}
              disabled={activeStep === 6}
              className="btn-primary text-xs disabled:opacity-40"
            >
              Next Relationship <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
