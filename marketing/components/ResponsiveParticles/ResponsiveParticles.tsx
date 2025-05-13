import React, { useEffect, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadSlim } from '@tsparticles/slim';

const ResponsiveParticles = () => {
  const [init, setInit] = useState(false);
  const [particleConfig, setParticleConfig] = useState({
    particles: {
      number: {
        value: 80,
      },
      size: {
        value: 50,
      },
    },
  });

  // Function to update particle configuration based on screen size
  const updateParticlesConfig = () => {
    const width = window.innerWidth;

    // Responsive configuration
    const config = {
      particles: {
        number: { value: 15 }, // Default value
        size: { value: 50 }, // Default value
      },
    };

    // For mobile devices
    if (width < 768) {
      config.particles.number.value = 20;
      config.particles.size.value = 40;
    }
    // For tablets
    else if (width >= 768 && width < 1024) {
      config.particles.number.value = 15;
      config.particles.size.value = 50;
    }
    // For desktops
    else if (width >= 1024 && width < 1440) {
      config.particles.number.value = 10;
      config.particles.size.value = 75;
    }
    // For large screens
    else {
      config.particles.number.value = 10;
      config.particles.size.value = 100;
    }

    setParticleConfig(config);
  };

  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadSlim(engine);
    }).then(() => {
      updateParticlesConfig();
      setInit(true);
    });
  }, []);

  if (init) {
    return (
      <Particles
        id="tsparticles"
        options={{
          particles: {
            number: { value: particleConfig.particles.number.value, density: { enable: true } },
            color: { value: '#ff7964' },
            shape: { type: 'circle' },
            opacity: {
              value: 0.15,
            },
            size: {
              value: particleConfig.particles.size.value,
            },
            move: {
              enable: true,
              speed: 0.5,
              direction: 'none',
              random: true,
              straight: false,
              attract: { enable: false },
            },
          },
          interactivity: {
            events: {
              onHover: { enable: true, mode: 'bubble' },
              onClick: { enable: true, mode: 'repulse' },
            },
            modes: {
              bubble: {
                distance: 300,
                size: particleConfig.particles.size.value * 0.8,
                duration: 5,
                opacity: 1,
                speed: 0.1,
              },
              repulse: { distance: 200, duration: 0.5 },
            },
          },
          retina_detect: true,
        }}
      />
    );
  }
};

export default ResponsiveParticles;
