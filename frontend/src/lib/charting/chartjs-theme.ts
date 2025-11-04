/**
 * Chart.js theme configuration
 * Applies default styling for charts across the application
 */
import { Chart as ChartJS } from 'chart.js';

export function applyChartJSTheme() {
  // Configure default Chart.js options
  ChartJS.defaults.responsive = true;
  ChartJS.defaults.maintainAspectRatio = false;
  ChartJS.defaults.font.family = 'system-ui, -apple-system, sans-serif';
  ChartJS.defaults.font.size = 12;
  ChartJS.defaults.color = '#6b7280'; // gray-500

  // Configure default plugin options
  if (ChartJS.defaults.plugins.legend) {
    ChartJS.defaults.plugins.legend.display = true;
    ChartJS.defaults.plugins.legend.position = 'top';
  }

  if (ChartJS.defaults.plugins.tooltip) {
    ChartJS.defaults.plugins.tooltip.enabled = true;
    ChartJS.defaults.plugins.tooltip.backgroundColor = 'rgba(17, 24, 39, 0.9)';
    ChartJS.defaults.plugins.tooltip.padding = 12;
    ChartJS.defaults.plugins.tooltip.cornerRadius = 6;
  }
}
