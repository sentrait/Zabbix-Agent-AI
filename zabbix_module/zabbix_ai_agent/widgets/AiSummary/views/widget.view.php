<?php
$summary = $data['summary'];

if (isset($summary['error'])): ?>
    <div style="padding: 20px; text-align: center; color: #dc2626;">
        <strong>⚠️ Error</strong><br>
        <?= htmlspecialchars($summary['error']) ?>
    </div>
<?php else: ?>
    <div style="padding: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #1f2937; line-height: 1.6;">
        
        <!-- Header -->
        <div style="margin-bottom: 20px; border-bottom: 2px solid #3b82f6; padding-bottom: 12px;">
            <h3 style="margin: 0; color: #1e40af; font-size: 18px; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 24px;">🤖</span>
                <?= htmlspecialchars($summary['title'] ?? 'Resumen Diario de IA') ?>
            </h3>
            <p style="margin: 4px 0 0 32px; font-size: 12px; color: #6b7280;">
                Generado: <?= date('d/m/Y H:i') ?>
            </p>
        </div>

        <!-- Overall Status -->
        <?php if (isset($summary['overall_status'])): ?>
        <div style="margin-bottom: 16px; padding: 12px; background: <?= $summary['overall_status']['color'] ?? '#f3f4f6' ?>; border-radius: 8px; border-left: 4px solid <?= $summary['overall_status']['border_color'] ?? '#9ca3af' ?>;">
            <strong style="font-size: 14px;"><?= htmlspecialchars($summary['overall_status']['label'] ?? 'Estado General') ?>:</strong>
            <span style="margin-left: 8px;"><?= htmlspecialchars($summary['overall_status']['description'] ?? '') ?></span>
        </div>
        <?php endif; ?>

        <!-- Critical Issues -->
        <?php if (!empty($summary['critical_issues'])): ?>
        <div style="margin-bottom: 16px;">
            <h4 style="margin: 0 0 8px 0; color: #dc2626; font-size: 15px;">🔴 Problemas Críticos</h4>
            <ul style="margin: 0; padding-left: 20px; font-size: 13px;">
                <?php foreach ($summary['critical_issues'] as $issue): ?>
                <li style="margin-bottom: 6px;">
                    <strong><?= htmlspecialchars($issue['name'] ?? '') ?></strong>
                    <?php if (isset($issue['description'])): ?>
                        <br><span style="color: #6b7280;"><?= htmlspecialchars($issue['description']) ?></span>
                    <?php endif; ?>
                </li>
                <?php endforeach; ?>
            </ul>
        </div>
        <?php endif; ?>

        <!-- Statistics -->
        <?php if (isset($summary['stats'])): ?>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px;">
            <?php foreach ($summary['stats'] as $stat): ?>
            <div style="text-align: center; padding: 12px; background: #f9fafb; border-radius: 6px; border: 1px solid #e5e7eb;">
                <div style="font-size: 24px; font-weight: bold; color: <?= $stat['color'] ?? '#3b82f6' ?>;">
                    <?= htmlspecialchars($stat['value'] ?? '0') ?>
                </div>
                <div style="font-size: 11px; color: #6b7280; margin-top: 4px;">
                    <?= htmlspecialchars($stat['label'] ?? '') ?>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>

        <!-- Recommendations -->
        <?php if (!empty($summary['recommendations'])): ?>
        <div style="margin-bottom: 16px;">
            <h4 style="margin: 0 0 8px 0; color: #059669; font-size: 15px;">💡 Recomendaciones de IA</h4>
            <ul style="margin: 0; padding-left: 20px; font-size: 13px;">
                <?php foreach ($summary['recommendations'] as $rec): ?>
                <li style="margin-bottom: 6px; color: #374151;">
                    <?= htmlspecialchars($rec) ?>
                </li>
                <?php endforeach; ?>
            </ul>
        </div>
        <?php endif; ?>

        <!-- Insights -->
        <?php if (isset($summary['insights'])): ?>
        <div style="padding: 12px; background: #eff6ff; border-radius: 6px; border-left: 3px solid #3b82f6; margin-top: 12px;">
            <strong style="color: #1e40af; font-size: 13px;">🔍 Análisis de IA:</strong>
            <p style="margin: 6px 0 0 0; font-size: 13px; color: #1f2937;">
                <?= nl2br(htmlspecialchars($summary['insights'])) ?>
            </p>
        </div>
        <?php endif; ?>

    </div>
<?php endif; ?>
