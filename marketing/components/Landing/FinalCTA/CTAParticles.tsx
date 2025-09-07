import React, { useEffect, useState } from 'react';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadSlim } from '@tsparticles/slim';
import classes from './CTAParticles.module.css';

type ParticleProps = {
  id: string;
  color: string;
  opacity: number;
};

const CTAParticles = ({ id, color, opacity }: ParticleProps) => {
  const [init, setInit] = useState(false);
  const [particleConfig, setParticleConfig] = useState({
    particles: {
      number: {
        value: 50,
      },
      size: {
        value: 30,
      },
    },
  });

  // Function to update particle configuration based on screen size
  const updateParticlesConfig = () => {
    const width = window.innerWidth;

    // Responsive configuration - fewer particles for CTA section
    const config = {
      particles: {
        number: { value: 12 }, // Default value - much fewer for contained area
        size: { value: 25 }, // Default value
      },
    };

    // For mobile devices
    if (width < 768) {
      config.particles.number.value = 6;
      config.particles.size.value = 25;
    }
    // For tablets
    else if (width >= 768 && width < 1024) {
      config.particles.number.value = 8;
      config.particles.size.value = 30;
    }
    // For desktops
    else if (width >= 1024 && width < 1440) {
      config.particles.number.value = 10;
      config.particles.size.value = 35;
    }
    // For large screens
    else {
      config.particles.number.value = 12;
      config.particles.size.value = 40;
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
      <div className={classes.container}>
        <Particles
          id={id}
          options={{
            fullScreen: {
              enable: false,
            },
            particles: {
              number: {
                value: particleConfig.particles.number.value,
              },
              color: { value: color },
              shape: { type: 'circle' },
              opacity: {
                value: opacity,
              },
              size: {
                value: particleConfig.particles.size.value,
              },
              move: {
                enable: true,
                speed: 0.8,
                direction: 'none',
                random: true,
                straight: false,
                attract: { enable: false },
                outModes: {
                  default: 'bounce',
                },
              },
            },
            interactivity: {
              events: {
                onHover: { enable: true, mode: 'bubble' },
                onClick: { enable: true, mode: 'repulse' },
              },
              modes: {
                bubble: {
                  distance: 200,
                  size: particleConfig.particles.size.value * 0.6,
                  duration: 3,
                  opacity: 0.8,
                  speed: 0.1,
                },
                repulse: { distance: 150, duration: 0.4 },
              },
            },
            detectRetina: true,
          }}
        />
      </div>
    );
  }

  return null;
};

export default CTAParticles;
