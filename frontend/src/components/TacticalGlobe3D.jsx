import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { MapPin, ShieldAlert, Radio, Crosshair, Activity, AlertCircle } from 'lucide-react';

const CRIME_HOTSPOTS = [
  {
    id: 'HOT-DELHI',
    city: 'New Delhi',
    lat: 28.6139,
    lng: 77.2090,
    threat_level: 'CRITICAL',
    syndicates: ['Shadow Syndicate (D-Nexus)', 'Inter-State Extortion Squad'],
    active_incidents: 4,
    cctns_ps: 'Connaught Place & Aerocity IGI PS',
    desc: 'High-profile extortion demands, burner SIM transmissions, black Fortuner ANPR sightings'
  },
  {
    id: 'HOT-MUMBAI',
    city: 'Mumbai',
    lat: 19.0760,
    lng: 72.8777,
    threat_level: 'HIGH',
    syndicates: ['Hawala Nexus', 'Shell Impex Front'],
    active_incidents: 3,
    cctns_ps: 'BKC Cyber Police & Fort PS',
    desc: 'Offshore ₹ 45 Cr trade layering through bogus MCA shell firms and HDFC bank conduits'
  },
  {
    id: 'HOT-BLR',
    city: 'Bengaluru',
    lat: 12.9716,
    lng: 77.5946,
    threat_level: 'HIGH',
    syndicates: ['Cyber-Cartel 09'],
    active_incidents: 5,
    cctns_ps: 'Koramangala Cyber Cell',
    desc: 'SIM mule aggregation, phishing gateways, Tron TRC-20 USDT crypto liquidation'
  },
  {
    id: 'HOT-HYD',
    city: 'Hyderabad',
    lat: 17.3850,
    lng: 78.4867,
    threat_level: 'MODERATE',
    syndicates: ['Mule Account Logistics'],
    active_incidents: 2,
    cctns_ps: 'Cyberabad Police Commissionerate',
    desc: 'Student bank account leasing rings used for second-layer money diversion'
  },
  {
    id: 'HOT-KOLKATA',
    city: 'Kolkata',
    lat: 22.5726,
    lng: 88.3639,
    threat_level: 'MODERATE',
    syndicates: ['Border Smuggling & FICN'],
    active_incidents: 1,
    cctns_ps: 'Lalbazar HQ',
    desc: 'Cross-border telecom routing and counterfeit currency transit point'
  }
];

// Convert Lat/Lng to 3D Cartesian coordinates on sphere
function latLngToVector3(lat, lng, radius) {
  const phi = (90 - lat) * (Math.PI / 180);
  const theta = (lng + 180) * (Math.PI / 180);
  const x = -(radius * Math.sin(phi) * Math.cos(theta));
  const z = radius * Math.sin(phi) * Math.sin(theta);
  const y = radius * Math.cos(phi);
  return new THREE.Vector3(x, y, z);
}

export default function TacticalGlobe3D({ onSelectCity }) {
  const mountRef = useRef(null);
  const [selectedHotspot, setSelectedHotspot] = useState(CRIME_HOTSPOTS[0]);
  const [radarActive, setRadarActive] = useState(true);

  useEffect(() => {
    if (!mountRef.current) return;
    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060a12);

    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(0, 40, 240);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    mountRef.current.appendChild(renderer.domElement);

    // Globe Base (Dark Sphere with Wireframe Grid)
    const globeRadius = 85;
    const globeGeom = new THREE.SphereGeometry(globeRadius, 36, 36);
    const globeMat = new THREE.MeshBasicMaterial({
      color: 0x09182a,
      wireframe: true,
      transparent: true,
      opacity: 0.35
    });
    const globe = new THREE.Mesh(globeGeom, globeMat);
    scene.add(globe);

    // Inner Glowing Atmosphere Core
    const innerGeom = new THREE.SphereGeometry(globeRadius - 1.5, 32, 32);
    const innerMat = new THREE.MeshBasicMaterial({
      color: 0x030712
    });
    const innerCore = new THREE.Mesh(innerGeom, innerMat);
    scene.add(innerCore);

    // Latitude / Longitude accent rings
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x00f2fe, wireframe: true, transparent: true, opacity: 0.25 });
    const ringGeom = new THREE.RingGeometry(globeRadius + 1, globeRadius + 2, 48);
    const ring = new THREE.Mesh(ringGeom, ringMat);
    ring.rotation.x = Math.PI / 2;
    scene.add(ring);

    // Hotspots Group
    const hotspotsGroup = new THREE.Group();
    scene.add(hotspotsGroup);

    // Add Hotspots Pins & Beacons
    CRIME_HOTSPOTS.forEach(spot => {
      const pos = latLngToVector3(spot.lat, spot.lng, globeRadius);

      const spotGroup = new THREE.Group();
      spotGroup.position.copy(pos);

      // Pin core
      const isCritical = spot.threat_level === 'CRITICAL';
      const colorHex = isCritical ? 0xff0055 : (spot.threat_level === 'HIGH' ? 0xf59e0b : 0x00f2fe);

      const pinGeom = new THREE.SphereGeometry(2.8, 16, 16);
      const pinMat = new THREE.MeshStandardMaterial({
        color: colorHex,
        emissive: colorHex,
        emissiveIntensity: 0.8
      });
      const pinMesh = new THREE.Mesh(pinGeom, pinMat);
      spotGroup.add(pinMesh);

      // Pulsing Radar Beacon Ring
      const beaconGeom = new THREE.RingGeometry(3.5, 5.0, 16);
      const beaconMat = new THREE.MeshBasicMaterial({
        color: colorHex,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.8
      });
      const beaconMesh = new THREE.Mesh(beaconGeom, beaconMat);
      beaconMesh.lookAt(new THREE.Vector3(0, 0, 0));
      beaconMesh.name = 'beacon';
      spotGroup.add(beaconMesh);

      // Projecting laser beam outwards
      const beamGeom = new THREE.CylinderGeometry(0.3, 0.3, 14, 8);
      const beamMat = new THREE.MeshBasicMaterial({ color: colorHex, transparent: true, opacity: 0.7 });
      const beam = new THREE.Mesh(beamGeom, beamMat);
      beam.position.copy(pos.clone().normalize().multiplyScalar(7));
      beam.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), pos.clone().normalize());
      scene.add(beam);

      spotGroup.userData = { spot };
      hotspotsGroup.add(spotGroup);
    });

    // Arc lines connecting Delhi <-> Mumbai <-> Bengaluru (Inter-state syndicate trail)
    const pDelhi = latLngToVector3(28.6139, 77.2090, globeRadius);
    const pMumbai = latLngToVector3(19.0760, 72.8777, globeRadius);
    const pBLR = latLngToVector3(12.9716, 77.5946, globeRadius);

    const createArc = (v1, v2, colorHex) => {
      const mid = new THREE.Vector3().addVectors(v1, v2).multiplyScalar(0.5);
      mid.multiplyScalar(1.22); // arch outwards
      const curve = new THREE.QuadraticBezierCurve3(v1, mid, v2);
      const geom = new THREE.BufferGeometry().setFromPoints(curve.getPoints(32));
      const mat = new THREE.LineBasicMaterial({ color: colorHex, transparent: true, opacity: 0.8 });
      return new THREE.Line(geom, mat);
    };

    scene.add(createArc(pDelhi, pMumbai, 0xff0055));
    scene.add(createArc(pMumbai, pBLR, 0x00f2fe));
    scene.add(createArc(pDelhi, pBLR, 0xf59e0b));

    // Interactive mouse rotation
    let isDragging = false;
    let prevMouse = { x: 0, y: 0 };

    const onMouseDown = (e) => {
      isDragging = true;
      prevMouse = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e) => {
      if (isDragging) {
        const dx = e.clientX - prevMouse.x;
        const dy = e.clientY - prevMouse.y;
        globe.rotation.y += dx * 0.006;
        innerCore.rotation.y += dx * 0.006;
        hotspotsGroup.rotation.y += dx * 0.006;
        prevMouse = { x: e.clientX, y: e.clientY };
      }
    };

    const onMouseUp = () => isDragging = false;

    // Hotspot click raycaster
    const onClick = (e) => {
      const rect = renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
      );
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(hotspotsGroup.children, true);

      if (intersects.length > 0) {
        let parent = intersects[0].object;
        while (parent && !parent.userData?.spot && parent.parent) {
          parent = parent.parent;
        }
        if (parent?.userData?.spot) {
          setSelectedHotspot(parent.userData.spot);
          if (onSelectCity) onSelectCity(parent.userData.spot.city);
        }
      }
    };

    const dom = renderer.domElement;
    dom.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    dom.addEventListener('click', onClick);

    // Set initial rotation so India faces front
    globe.rotation.y = -1.35;
    innerCore.rotation.y = -1.35;
    hotspotsGroup.rotation.y = -1.35;

    // Animation Loop
    let animId;
    let clock = new THREE.Clock();
    const animate = () => {
      animId = requestAnimationFrame(animate);
      const t = clock.getElapsedTime();

      // Slow idle orbit if not dragging
      if (!isDragging) {
        globe.rotation.y += 0.0015;
        innerCore.rotation.y += 0.0015;
        hotspotsGroup.rotation.y += 0.0015;
      }

      // Pulse beacon rings
      hotspotsGroup.children.forEach(group => {
        const beacon = group.getObjectByName('beacon');
        if (beacon) {
          const s = 1.0 + Math.sin(t * 4) * 0.35;
          beacon.scale.set(s, s, s);
        }
      });

      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(animId);
      dom.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      dom.removeEventListener('click', onClick);
      if (mountRef.current && dom) {
        mountRef.current.removeChild(dom);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
      {/* 3D Tactical Radar Canvas */}
      <div className="lg:col-span-8 relative h-[520px] rounded-xl overflow-hidden glass-panel border border-cyan-500/20">
        <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

        {/* Tactical Overlay Header */}
        <div className="absolute top-3 left-3 right-3 flex items-center justify-between p-3 glass-panel pointer-events-auto">
          <div className="flex items-center gap-2">
            <Radio className="w-4 h-4 text-cyan-400 animate-pulse" />
            <span className="font-display font-bold text-sm tracking-wide text-cyan-300">
              NATIONAL SURVEILLANCE RADAR (CCTNS / ICJS GRID)
            </span>
          </div>
          <span className="badge badge-cyber">
            <Activity className="w-3.5 h-3.5" /> 5 INTER-STATE HUBS ACTIVE
          </span>
        </div>

        {/* Radar instruction */}
        <div className="absolute bottom-3 left-3 p-2.5 glass-panel text-[11px] text-slate-300 pointer-events-auto">
          Rotate Globe to view Indian Crime Corridors. Click any beacon to inspect local syndicates.
        </div>
      </div>

      {/* Hotspot Intelligence Dossier */}
      <div className="lg:col-span-4 glass-panel p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
          <div className="flex items-center gap-2">
            <MapPin className="w-5 h-5 text-cyan-400" />
            <div>
              <h3 className="font-display font-bold text-base text-slate-100">{selectedHotspot.city} Corridor</h3>
              <p className="text-xs text-slate-400">{selectedHotspot.cctns_ps}</p>
            </div>
          </div>
          <span className={`badge ${selectedHotspot.threat_level === 'CRITICAL' ? 'badge-critical' : 'badge-high'}`}>
            {selectedHotspot.threat_level} THREAT
          </span>
        </div>

        <div className="text-xs text-slate-300 leading-relaxed bg-slate-900/60 p-3 rounded-lg border border-slate-800">
          {selectedHotspot.desc}
        </div>

        {/* Syndicates active in corridor */}
        <div>
          <h4 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider mb-2">Active Syndicates</h4>
          <div className="space-y-1.5">
            {selectedHotspot.syndicates.map((s, idx) => (
              <div key={idx} className="flex items-center justify-between text-xs bg-slate-800/50 px-3 py-2 rounded border border-slate-700/40">
                <span className="text-slate-200">{s}</span>
                <span className="text-cyan-400 font-mono text-[11px]">CCTNS Sync Active</span>
              </div>
            ))}
          </div>
        </div>

        {/* Inter-state corridor links */}
        <div className="pt-2 border-t border-slate-800">
          <h4 className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-2">Inter-State Corridor Links</h4>
          <div className="text-xs space-y-2 text-slate-300">
            <div className="p-2.5 rounded bg-slate-900/70 border-l-2 border-rose-500">
              <div className="font-semibold text-rose-400">Delhi ⟷ Mumbai Pipeline</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Extortion cash in Delhi is laundered via BKC shell entities into offshore accounts.</div>
            </div>
            <div className="p-2.5 rounded bg-slate-900/70 border-l-2 border-cyan-500">
              <div className="font-semibold text-cyan-400">Mumbai ⟷ Bengaluru Tech Line</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Phishing money converted to USDT TRC-20 and off-ramped to hawala operators.</div>
            </div>
          </div>
        </div>

        {/* Selectable Hotspot Switcher */}
        <div className="pt-2">
          <span className="text-[11px] text-slate-400 block mb-1.5 font-medium">Quick Select Corridor:</span>
          <div className="flex flex-wrap gap-1.5">
            {CRIME_HOTSPOTS.map(h => (
              <button
                key={h.id}
                onClick={() => {
                  setSelectedHotspot(h);
                  if (onSelectCity) onSelectCity(h.city);
                }}
                className={`text-xs px-2.5 py-1 rounded transition-all ${
                  selectedHotspot.id === h.id 
                    ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/50 font-semibold' 
                    : 'bg-slate-800/60 text-slate-400 hover:text-slate-200'
                }`}
              >
                {h.city}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
