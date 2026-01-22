<?php
namespace Modules\ZabbixAiAgent\Actions;

use CController;
use CControllerResponseData;

class AiAgentView extends CController {

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
        $data = [
            'iframe_url' => '/ai-backend/app/index.html' 
        ];
        
        $response = new CControllerResponseData($data);
        $response->setTitle('AI Agent');
        $this->setResponse($response);
    }
}
