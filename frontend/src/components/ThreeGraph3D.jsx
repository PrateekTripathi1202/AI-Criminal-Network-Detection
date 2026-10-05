import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { 
  Search, Shield, AlertTriangle, Filter, Eye, RefreshCw, ZoomIn, ZoomOut, Compass, Sparkles, User, Phone, Car, CreditCard, Building2, MapPin, Video
} from 'lucide-react';

const NODE_COLORS = {
  person: 0xff0055,       // Crimson
  phone: 0x00f2fe,        // Neon Cyan
  vehicle: 0xf59e0b,      // Amber
  account: 0x10b981,      // Emerald
  organization: 0x8b5cf6, // Violet
  location: 0xec4899,     // Pink
  cctv: 0x06b6d4          // Light Cyan
};

export default function ThreeGraph3D({ graphData, onSelectNode, selectedNodeId }) {
  const mountRef = useRef(null);
  const [filterType, setFilterType] = useState('ALL');
  const [filterSyndicate, setFilterSyndicate] = useState('ALL');
  const [minRisk, setMinRisk] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [hoveredNode, setHoveredNode] = useState(null);
  const [pathSource, setPathSource] = useState(null);
  const [pathTarget, setPathTarget] = useState(null);
  const [pathResult, setPathResult] = useState(null);
  const [cameraMode, setCameraMode] = useState('ORBIT');

  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const rendererRef = useRef(null);
  const nodesMeshGroupRef = useRef(new THREE.Group());
  const edgesMeshGroupRef = useRef(new THREE.Group());
  const particlesGroupRef = useRef(new THREE.Group());
  const nodeMapRef = useRef(new Map());
  const animFrameRef = useRef(null);

  // Filter nodes & edges
  const filteredNodes = (graphData?.nodes || []).filter(node => {
    if (filterType !== 'ALL' && node.type !== filterType) return false;
    if (filterSyndicate !== 'ALL' && node.syndicate !== filterSyndicate) return false;
    if ((node.risk_score || 0) < minRisk) return false;
    if (searchQuery.trim() && !node.label.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  const filteredNodeIds = new Set(filteredNodes.map(n => n.id));
  const filteredEdges = (graphData?.edges || []).filter(e => 
    filteredNodeIds.has(e.source) && filteredNodeIds.has(e.target)
  );

  useEffect(() => {
    if (!mountRef.current) return;
    const width = mountRef.current.clientWidth;
    const height = mountRef.current.clientHeight;

    // 1. Scene & Lighting
    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.background = new THREE.Color(0x070b14);
    scene.fog = new THREE.FogExp2(0x070b14, 0.0018);

    // Grid Floor
    const gridHelper = new THREE.GridHelper(500, 30, 0x1e293b, 0x0f172a);
    gridHelper.position.y = -120;
    scene.add(gridHelper);

    // 2. Camera
    const camera = new THREE.PerspectiveCamera(55, width / height, 1, 2000);
    camera.position.set(0, 80, 380);
    cameraRef.current = camera;

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0x00f2fe, 2.5, 600);
    pointLight1.position.set(150, 200, 150);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0xff0055, 2.0, 600);
    pointLight2.position.set(-150, -100, -150);
    scene.add(pointLight2);

    // Groups
    scene.add(nodesMeshGroupRef.current);
    scene.add(edgesMeshGroupRef.current);
    scene.add(particlesGroupRef.current);

    // 3. Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    mountRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Mouse Interaction (Orbit & Raycast)
    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };
    let spherical = { radius: 380, theta: 0.1, phi: Math.PI / 2.3 };

    const updateCameraFromSpherical = () => {
      camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
      camera.position.y = spherical.radius * Math.cos(spherical.phi);
      camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
      camera.lookAt(0, 0, 0);
    };
    updateCameraFromSpherical();

    const onMouseDown = (e) => {
      isDragging = true;
      previousMousePosition = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e) => {
      if (isDragging) {
        const deltaX = e.clientX - previousMousePosition.x;
        const deltaY = e.clientY - previousMousePosition.y;

        spherical.theta -= deltaX * 0.005;
        spherical.phi = Math.max(0.1, Math.min(Math.PI - 0.1, spherical.phi - deltaY * 0.005));
        updateCameraFromSpherical();
        previousMousePosition = { x: e.clientX, y: e.clientY };
      }

      // Raycasting for hover
      const rect = renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
      );

      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(nodesMeshGroupRef.current.children, true);

      if (intersects.length > 0) {
        const topObj = intersects[0].object;
        const nodeData = topObj.userData?.nodeData;
        if (nodeData) {
          setHoveredNode(nodeData);
          renderer.domElement.style.cursor = 'pointer';
        }
      } else {
        setHoveredNode(null);
        renderer.domElement.style.cursor = 'default';
      }
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const onWheel = (e) => {
      e.preventDefault();
      spherical.radius = Math.max(100, Math.min(900, spherical.radius + e.deltaY * 0.4));
      updateCameraFromSpherical();
    };

    const onClick = (e) => {
      const rect = renderer.domElement.getBoundingClientRect();
      const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
      );
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(nodesMeshGroupRef.current.children, true);

      if (intersects.length > 0) {
        const topObj = intersects[0].object;
        const nodeData = topObj.userData?.nodeData;
        if (nodeData) {
          onSelectNode(nodeData);
        }
      }
    };

    const dom = renderer.domElement;
    dom.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    dom.addEventListener('wheel', onWheel, { passive: false });
    dom.addEventListener('click', onClick);

    // Resize handler
    const handleResize = () => {
      if (!mountRef.current || !rendererRef.current) return;
      const w = mountRef.current.clientWidth;
      const h = mountRef.current.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    // Animation Loop
    let clock = new THREE.Clock();
    const animate = () => {
      animFrameRef.current = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Gentle auto-rotation when idle
      if (!isDragging) {
        spherical.theta += 0.001;
        updateCameraFromSpherical();
      }

      // Rotate nodes outer rings
      nodesMeshGroupRef.current.children.forEach(group => {
        const ring = group.getObjectByName('outerRing');
        if (ring) ring.rotation.z += 0.015;
        const pulse = group.getObjectByName('pulseGlow');
        if (pulse) {
          const s = 1.0 + Math.sin(elapsedTime * 3) * 0.15;
          pulse.scale.set(s, s, s);
        }
      });

      // Animate edge particles along curves
      particlesGroupRef.current.children.forEach(p => {
        if (p.userData?.curve) {
          p.userData.t = (p.userData.t + p.userData.speed) % 1.0;
          const pos = p.userData.curve.getPointAt(p.userData.t);
          p.position.copy(pos);
        }
      });

      renderer.render(scene, camera);
    };
    animate();

    return () => {
      cancelAnimationFrame(animFrameRef.current);
      dom.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      dom.removeEventListener('wheel', onWheel);
      dom.removeEventListener('click', onClick);
      window.removeEventListener('resize', handleResize);
      if (mountRef.current && dom) {
        mountRef.current.removeChild(dom);
      }
      renderer.dispose();
    };
  }, []);

  // Update 3D graph layout when filtered nodes/edges change
  useEffect(() => {
    const nodesGroup = nodesMeshGroupRef.current;
    const edgesGroup = edgesMeshGroupRef.current;
    const particlesGroup = particlesGroupRef.current;

    // Clear previous objects
    while (nodesGroup.children.length > 0) {
      nodesGroup.remove(nodesGroup.children[0]);
    }
    while (edgesGroup.children.length > 0) {
      edgesGroup.remove(edgesGroup.children[0]);
    }
    while (particlesGroup.children.length > 0) {
      particlesGroup.remove(particlesGroup.children[0]);
    }
    nodeMapRef.current.clear();

    if (!filteredNodes.length) return;

    // 1. Arrange nodes in a 3D spherical/force simulated shell
    const N = filteredNodes.length;
    const phiWeight = Math.PI * (3 - Math.sqrt(5)); // Golden ratio angle

    filteredNodes.forEach((node, i) => {
      const y = 1 - (i / (N - 1 || 1)) * 2; // y goes from 1 to -1
      const radiusAtY = Math.sqrt(1 - y * y);
      const theta = phiWeight * i;

      // Group layout radius by syndicate or type
      let sphereRadius = 140;
      if (node.type === 'person') sphereRadius = 90;
      if (node.type === 'phone' || node.type === 'vehicle') sphereRadius = 130;
      if (node.type === 'account' || node.type === 'organization') sphereRadius = 170;
      if (node.type === 'location' || node.type === 'cctv') sphereRadius = 210;

      const posX = Math.cos(theta) * radiusAtY * sphereRadius;
      const posY = y * sphereRadius;
      const posZ = Math.sin(theta) * radiusAtY * sphereRadius;

      const nodeGroup = new THREE.Group();
      nodeGroup.position.set(posX, posY, posZ);

      const colorHex = NODE_COLORS[node.type] || 0x38bdf8;
      const isSelected = selectedNodeId === node.id;
      const isKingpin = node.centrality?.kingpin_index > 25;

      // Inner Core Mesh (With Texture Support for Suspect Avatars)
      let geom;
      let mat;

      if (node.type === 'person') {
        geom = new THREE.SphereGeometry(isKingpin ? 12 : 9, 28, 28);
        if (node.metadata?.avatar) {
          const texture = new THREE.TextureLoader().load(node.metadata.avatar);
          mat = new THREE.MeshStandardMaterial({
            map: texture,
            roughness: 0.3,
            metalness: 0.5,
            emissive: colorHex,
            emissiveIntensity: isSelected ? 0.8 : 0.2
          });
        } else {
          mat = new THREE.MeshStandardMaterial({
            color: colorHex,
            roughness: 0.2,
            metalness: 0.8,
            emissive: colorHex,
            emissiveIntensity: isSelected ? 0.9 : (isKingpin ? 0.6 : 0.25)
          });
        }
      } else if (node.type === 'vehicle') {
        geom = new THREE.BoxGeometry(11, 8, 14);
        mat = new THREE.MeshStandardMaterial({
          color: colorHex,
          roughness: 0.2,
          metalness: 0.8,
          emissive: colorHex,
          emissiveIntensity: isSelected ? 0.9 : 0.3
        });
      } else if (node.type === 'account') {
        geom = new THREE.CylinderGeometry(8, 8, 4, 16);
        mat = new THREE.MeshStandardMaterial({
          color: colorHex,
          roughness: 0.2,
          metalness: 0.8,
          emissive: colorHex,
          emissiveIntensity: isSelected ? 0.9 : 0.3
        });
      } else if (node.type === 'organization') {
        geom = new THREE.OctahedronGeometry(9);
        mat = new THREE.MeshStandardMaterial({
          color: colorHex,
          roughness: 0.2,
          metalness: 0.8,
          emissive: colorHex,
          emissiveIntensity: isSelected ? 0.9 : 0.3
        });
      } else {
        geom = new THREE.SphereGeometry(6, 16, 16);
        mat = new THREE.MeshStandardMaterial({
          color: colorHex,
          roughness: 0.2,
          metalness: 0.8,
          emissive: colorHex,
          emissiveIntensity: isSelected ? 0.9 : 0.3
        });
      }
      const coreMesh = new THREE.Mesh(geom, mat);
      coreMesh.userData = { nodeData: node };
      nodeGroup.add(coreMesh);

      // Outer Hologram Orbit Ring
      const ringGeom = new THREE.RingGeometry(12, 14, 24);
      const ringMat = new THREE.MeshBasicMaterial({
        color: colorHex,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: isSelected ? 0.9 : 0.4
      });
      const ringMesh = new THREE.Mesh(ringGeom, ringMat);
      ringMesh.name = 'outerRing';
      nodeGroup.add(ringMesh);

      // Kingpin Glow Aura
      if (isKingpin || isSelected) {
        const glowGeom = new THREE.SphereGeometry(15, 16, 16);
        const glowMat = new THREE.MeshBasicMaterial({
          color: colorHex,
          transparent: true,
          opacity: 0.25,
          wireframe: true
        });
        const pulseGlow = new THREE.Mesh(glowGeom, glowMat);
        pulseGlow.name = 'pulseGlow';
        nodeGroup.add(pulseGlow);
      }

      nodesGroup.add(nodeGroup);
      nodeMapRef.current.set(node.id, { position: new THREE.Vector3(posX, posY, posZ), node });
    });

    // 2. Build Curved Edges & Flowing Particles
    filteredEdges.forEach(edge => {
      const src = nodeMapRef.current.get(edge.source);
      const tgt = nodeMapRef.current.get(edge.target);
      if (!src || !tgt) return;

      const p1 = src.position;
      const p2 = tgt.position;

      // Create quadratic bezier curve with mid-arch
      const mid = new THREE.Vector3().addVectors(p1, p2).multiplyScalar(0.5);
      const dist = p1.distanceTo(p2);
      mid.y += dist * 0.15; // gentle upward arc

      const curve = new THREE.QuadraticBezierCurve3(p1, mid, p2);
      const points = curve.getPoints(24);
      const lineGeom = new THREE.BufferGeometry().setFromPoints(points);

      const isMoney = edge.type.includes('transfer') || edge.type.includes('crypto');
      const edgeColor = isMoney ? 0x10b981 : (edge.type.includes('calls') ? 0x00f2fe : 0x475569);

      const lineMat = new THREE.LineBasicMaterial({
        color: edgeColor,
        transparent: true,
        opacity: 0.55
      });
      const line = new THREE.Line(lineGeom, lineMat);
      edgesGroup.add(line);

      // Animated glowing particle pulse along edge
      const particleGeom = new THREE.SphereGeometry(1.8, 8, 8);
      const particleMat = new THREE.MeshBasicMaterial({
        color: isMoney ? 0x34d399 : 0x38bdf8,
        transparent: true,
        opacity: 0.95
      });
      const particle = new THREE.Mesh(particleGeom, particleMat);
      particle.userData = {
        curve,
        t: Math.random(),
        speed: 0.005 + Math.random() * 0.006
      };
      particlesGroup.add(particle);
    });
  }, [filteredNodes.length, filteredEdges.length, selectedNodeId]);

  return (
    <div className="relative w-full h-[620px] rounded-xl overflow-hidden glass-panel border border-cyan-500/20">
      {/* 3D Canvas Mount */}
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {/* Top Controls Overlay */}
      <div className="absolute top-3 left-3 right-3 flex flex-wrap items-center justify-between gap-3 p-3 glass-panel z-10 pointer-events-auto">
        <div className="flex items-center gap-2 flex-1 min-w-[200px] max-w-sm bg-slate-900/80 px-3 py-1.5 rounded-lg border border-slate-700/60">
          <Search className="w-4 h-4 text-cyan-400" />
          <input
            type="text"
            placeholder="Search suspect, vehicle, burner SIM..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-transparent text-xs text-slate-100 placeholder-slate-400 focus:outline-none"
          />
        </div>

        {/* Entity Type Filter */}
        <div className="flex items-center gap-1.5 overflow-x-auto text-xs">
          {['ALL', 'person', 'phone', 'vehicle', 'account', 'location', 'cctv'].map(t => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                filterType === t 
                  ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/50 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              {t.toUpperCase()}
            </button>
          ))}
        </div>

        {/* Risk Filter */}
        <div className="flex items-center gap-2 text-xs text-slate-300 bg-slate-900/60 px-3 py-1 rounded-lg border border-slate-700/50">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
          <span>Risk &gt; {minRisk}%</span>
          <input 
            type="range" 
            min="0" 
            max="90" 
            step="10" 
            value={minRisk} 
            onChange={(e) => setMinRisk(Number(e.target.value))}
            className="w-16 accent-cyan-400 cursor-pointer"
          />
        </div>
      </div>

      {/* Floating 3D Legend & HUD */}
      <div className="absolute bottom-3 left-3 p-3 glass-panel text-xs text-slate-300 space-y-1.5 z-10 pointer-events-auto max-w-xs">
        <div className="font-semibold text-cyan-400 flex items-center gap-1.5 pb-1 border-b border-slate-700/60">
          <Compass className="w-3.5 h-3.5" /> 3D KNOWLEDGE GRAPH HUD
        </div>
        <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[11px]">
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#ff0055]" /> Person / Suspect</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#00f2fe]" /> CDR / Burner Phone</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#f59e0b]" /> ANPR Tracked Vehicle</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#10b981]" /> Bank / Hawala Account</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#8b5cf6]" /> Shell / Front Org</span>
          <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-[#ec4899]" /> Hotspot Location</span>
        </div>
        <div className="text-[10px] text-slate-400 pt-1 border-t border-slate-800">
          💡 Click node for Full Dossier. Drag mouse to 3D Orbit. Scroll to Zoom.
        </div>
      </div>

      {/* Hover Node Tooltip */}
      {hoveredNode && (
        <div className="absolute bottom-3 right-3 p-3 glass-panel-glow bg-slate-950/90 text-xs text-slate-100 z-10 max-w-xs pointer-events-none animate-fadeIn">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="font-bold text-cyan-300">{hoveredNode.label}</span>
            <span className={`badge ${hoveredNode.risk_score > 80 ? 'badge-critical' : 'badge-high'}`}>
              Risk: {hoveredNode.risk_score}%
            </span>
          </div>
          <div className="text-slate-400 text-[11px] mb-1">
            Type: <span className="text-slate-200 capitalize">{hoveredNode.type}</span> | Syndicate: <span className="text-slate-200">{hoveredNode.syndicate}</span>
          </div>
          {hoveredNode.metadata?.alias && (
            <div className="text-[11px] text-amber-300">Alias: {hoveredNode.metadata.alias}</div>
          )}
          {hoveredNode.centrality?.kingpin_index && (
            <div className="text-[11px] text-cyan-400 font-mono mt-1">
              Kingpin Index: {hoveredNode.centrality.kingpin_index} | Rank: High Authority
            </div>
          )}
        </div>
      )}
    </div>
  );
}
