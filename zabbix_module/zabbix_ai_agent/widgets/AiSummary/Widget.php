<?php declare(strict_types = 0);

namespace Modules\ZabbixAiAgent\Widgets\AiSummary;

use Zabbix\Core\CWidget;

class Widget extends CWidget {

    public function getDefaultName(): string {
        return _('AI Daily Summary');
    }
}
