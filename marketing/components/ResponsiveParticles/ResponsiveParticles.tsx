import React, { useEffect, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadSlim } from '@tsparticles/slim';
import { useDebouncedCallback } from 'use-debounce';

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
  const updateParticlesConfig = useDebouncedCallback(() => {
    const width = window.innerWidth;

    // Responsive configuration
    const config = {
      particles: {
        number: { value: 80 }, // Default value
        size: { value: 50 }, // Default value
      },
    };

    // For mobile devices
    if (width < 768) {
      config.particles.number.value = 30;
      config.particles.size.value = 40;
    }
    // For tablets
    else if (width >= 768 && width < 1024) {
      config.particles.number.value = 30;
      config.particles.size.value = 50;
    }
    // For desktops
    else if (width >= 1024 && width < 1440) {
      config.particles.number.value = 30;
      config.particles.size.value = 75;
    }
    // For large screens
    else {
      config.particles.number.value = 30;
      config.particles.size.value = 100;
    }

    setParticleConfig(config);
  }, 500);

  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadSlim(engine);
    }).then(() => {
      setInit(true);
    });
  }, []);

  // Effect to handle window resize
  useEffect(() => {
    // Initial configuration
    updateParticlesConfig();

    // Add event listener for window resize
    window.addEventListener('resize', updateParticlesConfig);

    // Cleanup
    return () => {
      window.removeEventListener('resize', updateParticlesConfig);
    };
  }, [updateParticlesConfig]);

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
            line_linked: {
              enable: true,
              distance: 150,
              color: '#ffffff',
              opacity: 0.4,
              width: 1,
            },
            move: {
              enable: true,
              speed: 0.5,
              direction: 'none',
              random: false,
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
              grab: { distance: 400, line_linked: { opacity: 1 } },
              bubble: {
                distance: 300,
                size: particleConfig.particles.size.value * 0.8,
                duration: 5,
                opacity: 1,
                speed: 0.1,
              },
              repulse: { distance: 200, duration: 0.4 },
              push: { particles_nb: 4 },
              remove: { particles_nb: 2 },
            },
          },
          retina_detect: true,
        }}
      />
    );
  }
};

export default ResponsiveParticles;
