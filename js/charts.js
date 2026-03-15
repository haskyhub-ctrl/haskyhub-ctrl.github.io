/**
 * FRAS Charts JS
 * Chart.js wrapper functions
 */

const chartColors = {
    red: '#ef4444',
    orange: '#f97316',
    yellow: '#eab308',
    green: '#22c55e',
    blue: '#3b82f6',
    purple: '#8b5cf6',
    cyan: '#06b6d4',
    pink: '#ec4899',
};

const riskColors = {
    low: '#22c55e',
    medium: '#eab308',
    high: '#f97316',
    critical: '#ef4444',
};

function getChartDefaults() {
    return {
        color: '#94a3b8',
        borderColor: 'rgba(255,255,255,0.1)',
        font: { family: 'Inter, sans-serif' },
    };
}

/**
 * Create a radar chart for category scores
 */
function createRadarChart(canvasId, categoryScores, label = 'Điểm đánh giá') {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const labels = categoryScores.map(c => c.category_name || c.name || '');
    const data = categoryScores.map(c => c.percentage);
    const colors = categoryScores.map(c => riskColors[c.risk_level] || '#94a3b8');

    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: 'rgba(249, 115, 22, 0.15)',
                borderColor: '#f97316',
                borderWidth: 2,
                pointBackgroundColor: colors,
                pointBorderColor: colors,
                pointRadius: 5,
                pointHoverRadius: 7,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 25,
                        color: '#64748b',
                        backdropColor: 'transparent',
                        font: { size: 10 },
                    },
                    grid: { color: 'rgba(255,255,255,0.08)' },
                    pointLabels: {
                        color: '#cbd5e1',
                        font: { size: 11, weight: '500' },
                    },
                    angleLines: { color: 'rgba(255,255,255,0.06)' },
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => `${ctx.parsed.r}% nguy cơ`
                    }
                }
            }
        }
    });
}

/**
 * Create a doughnut chart for risk gauge
 */
function createRiskGauge(canvasId, percentage, riskLevel) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const color = riskColors[riskLevel] || '#94a3b8';

    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Nguy cơ', 'An toàn'],
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: [color, 'rgba(255,255,255,0.05)'],
                borderWidth: 0,
                cutout: '75%',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false },
            },
        },
        plugins: [{
            id: 'centerText',
            afterDraw: (chart) => {
                const { ctx, chartArea } = chart;
                const cx = (chartArea.left + chartArea.right) / 2;
                const cy = (chartArea.top + chartArea.bottom) / 2;

                ctx.save();
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                ctx.font = 'bold 28px Inter, sans-serif';
                ctx.fillStyle = color;
                ctx.fillText(`${percentage}%`, cx, cy - 8);

                ctx.font = '12px Inter, sans-serif';
                ctx.fillStyle = '#94a3b8';
                ctx.fillText('Tỷ lệ nguy cơ', cx, cy + 18);

                ctx.restore();
            }
        }]
    });
}

/**
 * Create a bar chart for category comparison
 */
function createBarChart(canvasId, categoryScores) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categoryScores.map(c => c.category_name || ''),
            datasets: [{
                label: 'Tỷ lệ nguy cơ (%)',
                data: categoryScores.map(c => c.percentage),
                backgroundColor: categoryScores.map(c => riskColors[c.risk_level] || '#94a3b8'),
                borderRadius: 6,
                maxBarThickness: 40,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255,255,255,0.05)' },
                },
                y: {
                    ticks: { color: '#cbd5e1', font: { size: 11 } },
                    grid: { display: false },
                }
            },
            plugins: {
                legend: { display: false },
            }
        }
    });
}

/**
 * Create a line chart for historical trends
 */
function createLineChart(canvasId, assessments) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const labels = assessments.map(a => formatDate(a.completed_at || a.created_at));
    const data = assessments.map(a => a.risk_percentage);

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Tỷ lệ nguy cơ (%)',
                data: data,
                borderColor: '#f97316',
                backgroundColor: 'rgba(249, 115, 22, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointBackgroundColor: '#f97316',
                pointBorderColor: '#f97316',
                pointHoverRadius: 7,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255,255,255,0.05)' },
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255,255,255,0.05)' },
                }
            },
            plugins: {
                legend: { display: false },
            }
        }
    });
}

/**
 * Create overlay radar for comparison
 */
function createCompareRadar(canvasId, datasets) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;

    const colors = ['#f97316', '#3b82f6', '#22c55e', '#8b5cf6'];

    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: datasets[0]?.labels || [],
            datasets: datasets.map((ds, i) => ({
                label: ds.label,
                data: ds.data,
                backgroundColor: `${colors[i % colors.length]}20`,
                borderColor: colors[i % colors.length],
                borderWidth: 2,
                pointRadius: 4,
                pointBackgroundColor: colors[i % colors.length],
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: '#64748b', backdropColor: 'transparent' },
                    grid: { color: 'rgba(255,255,255,0.08)' },
                    pointLabels: { color: '#cbd5e1', font: { size: 11 } },
                    angleLines: { color: 'rgba(255,255,255,0.06)' },
                }
            },
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#cbd5e1' }
                },
            }
        }
    });
}
