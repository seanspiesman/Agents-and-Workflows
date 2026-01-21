# Phase 3: Architectural Design - The Blues Harmonica Shed

## System Architecture Overview

### High-Level Architecture
```
┌───────────────────────────────────────────────────────────────┐
│                    Client Application (Browser)                │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │   React UI   │    │ Audio Core  │    │ Visualization  │  │
│  │ (TSX)        │    │ (Web Audio)│    │   System       │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        ▲                  ▲                     ▲            │
│        │                  │                     │            │
└────────┼──────────────────┼─────────────────┼───────────┘
         │                  │                     │            
         ▼                  ▼                     ▼            
┌───────────────────────────────────────────────────────────────┐
│                    State Management Layer                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     React Context                        │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
         ▲                  ▲                     ▲            
         │                  │                     │            
┌────────┴──────────────────┴─────────────────┴───────────┐
│                    Data Layer                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │ LocalStorage│    │ Audio Buffers│    │ Texture     │  │
│  │ (User Prefs)│    │ (Preloaded) │    │ Assets      │  │
│  └─────────────┘    └─────────────┘    └─────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. React Application Structure
```
src/
├── components/          # Reusable UI components
│   ├── ui/              # Basic UI elements (buttons, sliders)
│   ├── visualization/   # Audio visualizations
│   └── layout/          # Page layouts and containers
|
├── features/            # Feature-specific components
│   ├── lick-library/    # The Lick Library UI
│   ├── virtual-monitor/ # Web-Based Virtual Monitor
│   ├── jam-room/        # The Jam Room player
│   ├── amp-room/        # The Amp Room simulator
│   └── ai-practice/     # AI Call & Response
|
├── hooks/               # Custom React hooks
│   ├── useAudio.js      # Audio context management
│   ├── useVisualization.js # Visualization state
│   └── useLickLibrary.js  # Lick library data
|
├── context/             # React Context providers
│   ├── AudioContext.js  # Global audio state
│   └── AppState.js      # Application-wide state
|
├── pages/               # Main application pages
│   ├── Home.js          # Landing page
│   ├── Library.js       # Lick library page
│   ├── Practice.js      # Practice area
│   └── Settings.js      # User settings
|
├── utils/               # Utility functions
│   ├── audio.js         # Audio processing helpers
│   └── visualization.js # Visualization utilities
|
└── App.jsx             # Main application component
```

### 2. Audio Processing Architecture
```
┌───────────────────────────────────────────────────────────────┐
│                    Audio Processing Pipeline                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Input       │    │ Processing  │    │ Output          │  │
│  │ (Microphone)│───▶│   Nodes     │───▶│    Speakers    │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        ▲                  ▲                     ▲            │
│        │                  │                     │            │
└────────┼──────────────────┼─────────────────┼───────────┘
         │                  │                     │            
         ▼                  ▼                     ▼            
┌───────────────────────────────────────────────────────────────┐
│                    Audio Worklet Processor                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     Pitch Detection                      │  │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │  │
│  │  │ YIN Alg.   │    │ Auto-       │    │ Harmonic   │  │  │
│  │  │            │    │ correlation │    │ Product    │  │  │
│  │  └─────────────┘    └─────────────┘    └─────────────┘  │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

### 3. Visualization Architecture
```
┌───────────────────────────────────────────────────────────────┐
│                    Visualization System                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Canvas API  │    │ WebGL       │    │ CSS Animations  │  │
│  │ (Main)      │    │ (Fallback)  │    │ (UI Elements)   │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        ▲                  ▲                     ▲            │
│        │                  │                     │            │
└────────┼──────────────────┼─────────────────┼───────────┘
         │                  │                     │            
         ▼                  ▼                     ▼            
┌───────────────────────────────────────────────────────────────┐
│                    Rendering Pipeline                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     requestAnimationFrame                │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## State Management Strategy

### React Context Architecture
```javascript
// AudioContext.js
const AudioContext = React.createContext();

function AudioProvider({ children }) {
  const [audioContext, setAudioContext] = useState(null);
  const [analyserNode, setAnalyserNode] = useState(null);
  const [audioWorklet, setAudioWorklet] = useState(null);
  
  const initializeAudio = async () => {
    try {
      const context = new (window.AudioContext || window.webkitAudioContext)(
        { sampleRate: 44100, latencyHint: "playback" }
      );
      
      const analyser = context.createAnalyser();
      analyser.fftSize = 2048;
      
      await context.audioWorklet.addModule('audio-worklet.js');
      const worklet = new AudioWorkletNode(context, 'pitch-detector');
      
      setAudioContext(context);
      setAnalyserNode(analyser);
      setAudioWorklet(worklet);
    } catch (error) {
      console.error('Audio initialization failed:', error);
    }
  };
  
  return (
    <AudioContext.Provider value={{ audioContext, analyserNode, audioWorklet }}>
      {children}
    </AudioContext.Provider>
  );
}
```

### State Management Patterns
1. **Global State**: React Context for audio processing state
2. **Local State**: useState for component-specific state
3. **Derived State**: Memoized values with useMemo
4. **Effect Management**: useEffect for side effects
5. **Custom Hooks**: Encapsulate complex state logic

## Audio Processing Architecture

### Web Audio Graph Design
```
┌───────────────────────────────────────────────────────────────┐
│                    Web Audio Graph                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Input       │    │ Processing  │    │ Output          │  │
│  │ (Microphone)│───▶│   Nodes     │───▶│    Speakers    │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        ▲                  ▲                     ▲            │
│        │                  │                     │            │
└────────┼──────────────────┼─────────────────┼───────────┘
         │                  │                     │            
         ▼                  ▼                     ▼            
┌───────────────────────────────────────────────────────────────┐
│                    Node Connections                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     Microphone → GainNode                │  │
│  │                     GainNode → AnalyserNode              │  │
│  │                     AnalyserNode → AudioWorkletNode       │  │
│  │                     AudioWorkletNode → GainNode          │  │
│  │                     GainNode → DestinationNode            │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

### Audio Worklet Architecture
```javascript
// audio-worklet.js
class PitchDetector extends AudioWorkletProcessor {
  static get parameterDescriptors() {
    return [
      { name: 'threshold', defaultValue: 0.5, minValue: 0, maxValue: 1 },
    ];
  }
  
  process(inputs, outputs) {
    const input = inputs[0];
    if (input.length === 0) return;
    
    const channelData = input[0];
    // YIN algorithm implementation
    const pitch = this.detectPitch(channelData);
    
    // Send pitch data to main thread
    this.port.postMessage({ pitch, timestamp: this.sampleTime });
    
    return true;
  }
  
  detectPitch(buffer) {
    // YIN algorithm implementation
    // Returns fundamental frequency in Hz
  }
}

registerProcessor('pitch-detector', PitchDetector);
```

## Visualization Architecture

### Canvas Rendering Pipeline
```javascript
// visualization.js
class AudioVisualizer {
  constructor(canvas, analyserNode) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.analyserNode = analyserNode;
    this.dataArray = new Uint8Array(analyserNode.frequencyBinCount);
  }
  
  render() {
    requestAnimationFrame(() => this.render());
    
    // Clear canvas
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
    // Get frequency data
    this.analyserNode.getByteFrequencyData(this.dataArray);
    
    // Draw frequency visualization
    this.drawFrequencyBars();
    
    // Draw waveform
    this.drawWaveform();
  }
  
  drawFrequencyBars() {
    // Draw bar visualization for frequency spectrum
  }
  
  drawWaveform() {
    // Draw waveform visualization
  }
}
```

### WebGL Fallback Architecture
```javascript
// webgl-visualization.js
class WebGLVisualizer {
  constructor(canvas, analyserNode) {
    this.canvas = canvas;
    this.gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    this.analyserNode = analyserNode;
    this.dataArray = new Uint8Array(analyserNode.frequencyBinCount);
    
    // Initialize WebGL program
    this.initShaders();
  }
  
  initShaders() {
    // Compile vertex and fragment shaders
    // Create particle system for visualization
  }
  
  render() {
    requestAnimationFrame(() => this.render());
    
    // Get frequency data
    this.analyserNode.getByteFrequencyData(this.dataArray);
    
    // Update particle positions based on frequency data
    this.updateParticles();
    
    // Draw particles with WebGL
    this.drawParticles();
  }
}
```

## Performance Optimization Strategy

### Audio Processing Optimizations
1. **Buffer Size**: 2048 samples for good frequency resolution
2. **Sample Rate**: 44.1kHz standard (48kHz for professional audio)
3. **Latency**: <20ms target with lowLatency hint
4. **Worklet Processing**: Efficient C++-like processing in JavaScript
5. **Node Management**: Proper disconnection with disconnect() method

### Visualization Optimizations
1. **Canvas Rendering**: requestAnimationFrame for smooth animation
2. **Double Buffering**: Avoid tearing and visual artifacts
3. **Performance Monitoring**: Frame rate tracking with performance.now()
4. **Complexity Management**: Reduce visualization complexity when needed
5. **WebGL Fallback**: For complex visualizations on low-end devices

### Memory Management Strategy
1. **Audio Buffer Cleanup**: Proper cleanup after use
2. **Node Disconnection**: disconnect() method for all nodes
3. **Memory Monitoring**: Chrome DevTools memory profiler
4. **Heap Snapshots**: Regular memory usage tracking
5. **Garbage Collection**: Manual GC when needed for critical sections

## Error Handling and Recovery Strategy

### Audio Context Suspension
```javascript
// audio-context-manager.js
class AudioContextManager {
  constructor() {
    this.audioContext = null;
    this.resumePromise = null;
  }
  
  async initialize() {
    try {
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)(
        { sampleRate: 44100, latencyHint: "playback" }
      );
      
      // Handle suspension
      this.audioContext.addEventListener('statechange', () => {
        if (this.audioContext.state === 'suspended') {
          this.resumePromise = this.audioContext.resume();
        }
      });
    } catch (error) {
      console.error('AudioContext initialization failed:', error);
      throw error;
    }
  }
  
  async resume() {
    if (this.audioContext.state === 'suspended') {
      await this.resumePromise;
    }
  }
}
```

### Error Recovery Patterns
1. **Graceful Degradation**: Fallback to simpler implementations
2. **User Notification**: Clear error messages with recovery options
3. **State Restoration**: Return to known good state after errors
4. **Retry Logic**: Automatic retry for transient failures
5. **Fallback Modes**: Reduced functionality when primary features fail

## Testing Strategy

### Unit Testing Architecture
```javascript
// audio-processing.test.js
describe('Audio Processing', () => {
  let audioContext;
  
  beforeEach(() => {
    audioContext = new AudioContext();
  });
  
  afterEach(() => {
    audioContext.close();
  });
  
  test('should detect pitch accurately', () => {
    // Test pitch detection with known frequencies
  });
  
  test('should process audio with low latency', () => {
    // Test processing latency
  });
  
  test('should handle audio context suspension', () => {
    // Test suspension and resume
  });
});
```

### Integration Testing Strategy
1. **Web Audio Graph**: Verify node connections and data flow
2. **Component Interactions**: Test UI and audio processing integration
3. **State Management**: Verify React Context state updates
4. **Visualization**: Test rendering performance and accuracy
5. **Error Handling**: Verify error recovery and fallback modes

### End-to-End Testing Strategy
1. **User Workflows**: Complete workflows from start to finish
2. **Performance Testing**: Load testing and stress scenarios
3. **Browser Compatibility**: Cross-browser testing matrix
4. **Accessibility Testing**: WCAG AA compliance verification
5. **User Acceptance**: Final validation with target users

## Deployment Strategy

### Local Development Setup
1. **Vite Configuration**: Optimized for React + TypeScript
2. **Development Server**: Hot module replacement enabled
3. **Source Maps**: For debugging and profiling
4. **Error Overlay**: Development-only error messages
5. **Performance Monitoring**: Built-in performance tracking

### Production Build Optimization
1. **Code Splitting**: Route-based chunking for faster loads
2. **Tree Shaking**: Remove unused code with rollup
3. **Minification**: Production-optimized builds
4. **Compression**: Brotli compression for assets
5. **Caching**: Long-term caching headers

### Local Deployment Strategy
1. **Local Server**: Serve application on localhost
2. **Asset Preloading**: Cache audio assets locally
3. **Offline Support**: Service worker for offline access
4. **Progressive Enhancement**: Graceful degradation when features unavailable
5. **Local Storage**: User preferences stored locally

## Next Steps
1. Begin Phase 4: Master Planning
2. Create detailed implementation plan
3. Establish coding standards and conventions
4. Set up development environment and tooling
5. Begin prototyping key components