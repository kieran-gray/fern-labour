import bundleAnalyzer from '@next/bundle-analyzer';

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
});

export default withBundleAnalyzer({
  reactStrictMode: false,
  output: 'export',
  eslint: {
    ignoreDuringBuilds: true,
  },
  compress: false,
  experimental: {
    optimizePackageImports: ['@mantine/core', '@mantine/hooks', '@mantine/carousel', '@tabler/icons-react']
  },
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },
});
