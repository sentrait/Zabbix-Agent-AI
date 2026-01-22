<?php declare(strict_types = 1);

namespace Modules\ZabbixAiAgent\Actions;

use CController;
use CControllerResponseData;

class AiDashboard extends CController {

    protected function init(): void {
        $this->disableCsrfValidation();
    }

    protected function checkInput(): bool {
        return true;
    }

    protected function checkPermissions(): bool {
        return true;
    }

    protected function doAction(): void {
        // Get AI summary from backend
        $summary = $this->getAiSummary();
        
        $response = new CControllerResponseData([
            'summary' => $summary,
            'title' => 'AI Dashboard - Resumen Diario'
        ]);
        
        $response->setTitle('AI Dashboard');
        $this->setResponse($response);
    }
    
    private function getAiSummary(): array {
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
                return $data ?: ['error' => 'Invalid response'];
            }
            
            return ['error' => 'AI service unavailable'];
            
        } catch (Exception $e) {
            return ['error' => $e->getMessage()];
        }
    }
}
