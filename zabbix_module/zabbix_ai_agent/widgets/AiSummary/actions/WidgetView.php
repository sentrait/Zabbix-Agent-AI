<?php declare(strict_types = 0);

namespace Modules\ZabbixAiAgent\Widgets\AiSummary\Actions;

use CControllerDashboardWidgetView;
use CControllerResponseData;

class WidgetView extends CControllerDashboardWidgetView {

    protected function doAction(): void {
        // Fetch AI summary from backend
        $summary_data = $this->getAiSummary();
        
        $this->setResponse(new CControllerResponseData([
            'name' => $this->getInput('name', $this->widget->getDefaultName()),
            'summary' => $summary_data,
            'user' => [
                'debug_mode' => $this->getDebugMode()
            ]
        ]));
    }
    
    private function getAiSummary(): array {
        // Call AI backend to get daily summary
        $backend_url = 'http://localhost:8000/api/summary/daily';
        
        try {
            $ch = curl_init($backend_url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_TIMEOUT, 5);
            
            $response = curl_exec($ch);
            $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            curl_close($ch);
            
            if ($http_code === 200 && $response) {
                $data = json_decode($response, true);
                return $data ?: ['error' => 'Invalid response from AI service'];
            }
            
            return ['error' => 'AI service unavailable (HTTP ' . $http_code . ')'];
            
        } catch (Exception $e) {
            return ['error' => 'Failed to connect to AI service: ' . $e->getMessage()];
        }
    }
}
