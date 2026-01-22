<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= htmlspecialchars($data['title']) ?></title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8fafc;
            color: #1f2937;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .header h1 {
            margin: 0;
            font-size: 32px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header .subtitle {
            opacity: 0.9;
            margin-top: 8px;
            font-size: 14px;
        }
        
        .status-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 6px solid;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .stat-value {
            font-size: 36px;
            font-weight: bold;
            margin: 8px 0;
        }
        
        .stat-label {
            font-size: 13px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .issue-list {
            list-style: none;
            padding: 0;
            margin: 16px 0;
        }
        
        .issue-item {
            padding: 12px 16px;
            background: #f9fafb;
            border-radius: 8px;
            margin-bottom: 8px;
            border-left: 3px solid #ef4444;
        }
        
        .issue-item strong {
            display: block;
            margin-bottom: 4px;
        }
        
        .recommendations {
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .recommendations h3 {
            margin-top: 0;
            color: #1e40af;
        }
        
        .insights {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            border: 2px solid #f59e0b;
        }
        
        .error {
            background: #fee2e2;
            color: #991b1b;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <?php $summary = $data['summary']; ?>
        
        <?php if (isset($summary['error'])): ?>
            <div class="error">
                <h2>⚠️ Error</h2>
                <p><?= htmlspecialchars($summary['error']) ?></p>
            </div>
        <?php else: ?>
            
            <!-- Header -->
            <div class="header">
                <h1>
                    <span style="font-size: 40px;">🤖</span>
                    <?= htmlspecialchars($summary['title'] ?? 'Resumen Diario de IA') ?>
                </h1>
                <div class="subtitle">
                    Generado automáticamente el <?= date('d/m/Y') ?> a las <?= date('H:i') ?>
                </div>
            </div>

            <!-- Overall Status -->
            <?php if (isset($summary['overall_status'])): ?>
            <div class="status-card" style="border-left-color: <?= $summary['overall_status']['border_color'] ?? '#9ca3af' ?>; background: <?= $summary['overall_status']['color'] ?? '#fff' ?>;">
                <h2 style="margin: 0 0 8px 0;"><?= htmlspecialchars($summary['overall_status']['label'] ?? 'Estado General') ?></h2>
                <p style="margin: 0; font-size: 16px;"><?= htmlspecialchars($summary['overall_status']['description'] ?? '') ?></p>
            </div>
            <?php endif; ?>

            <!-- Statistics -->
            <?php if (isset($summary['stats'])): ?>
            <div class="stats-grid">
                <?php foreach ($summary['stats'] as $stat): ?>
                <div class="stat-card">
                    <div class="stat-label"><?= htmlspecialchars($stat['label'] ?? '') ?></div>
                    <div class="stat-value" style="color: <?= $stat['color'] ?? '#3b82f6' ?>;">
                        <?= htmlspecialchars($stat['value'] ?? '0') ?>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>

            <!-- Critical Issues -->
            <?php if (!empty($summary['critical_issues'])): ?>
            <div class="status-card" style="border-left-color: #ef4444;">
                <h3 style="margin: 0 0 16px 0; color: #dc2626;">🔴 Problemas Críticos</h3>
                <ul class="issue-list">
                    <?php foreach ($summary['critical_issues'] as $issue): ?>
                    <li class="issue-item">
                        <strong><?= htmlspecialchars($issue['name'] ?? '') ?></strong>
                        <?php if (isset($issue['description'])): ?>
                            <small style="color: #6b7280;"><?= htmlspecialchars($issue['description']) ?></small>
                        <?php endif; ?>
                    </li>
                    <?php endforeach; ?>
                </ul>
            </div>
            <?php endif; ?>

            <!-- AI Insights -->
            <?php if (isset($summary['insights'])): ?>
            <div class="insights">
                <h3 style="margin: 0 0 12px 0; color: #92400e;">
                    <span style="font-size: 20px;">🔍</span> Análisis de IA
                </h3>
                <p style="margin: 0; line-height: 1.6; color: #78350f;">
                    <?= nl2br(htmlspecialchars($summary['insights'])) ?>
                </p>
            </div>
            <?php endif; ?>

            <!-- Recommendations -->
            <?php if (!empty($summary['recommendations'])): ?>
            <div class="recommendations">
                <h3><span style="font-size: 20px;">💡</span> Recomendaciones</h3>
                <ul style="line-height: 1.8;">
                    <?php foreach ($summary['recommendations'] as $rec): ?>
                    <li><?= htmlspecialchars($rec) ?></li>
                    <?php endforeach; ?>
                </ul>
            </div>
            <?php endif; ?>

        <?php endif; ?>
    </div>
</body>
</html>
