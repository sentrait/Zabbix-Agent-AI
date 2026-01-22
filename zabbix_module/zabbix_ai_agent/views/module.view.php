<?php
/** @var CView $this */

// Direct HTML output for now to debug
echo '<div style="width:100%; height:100%; padding: 10px;">';
echo '<h3>AI Agent</h3>';
echo '<iframe src="' . htmlspecialchars($data['iframe_url']) . '" style="width: 100%; height: calc(100vh - 150px); border: none; border-radius: 8px;"></iframe>';
echo '</div>';
