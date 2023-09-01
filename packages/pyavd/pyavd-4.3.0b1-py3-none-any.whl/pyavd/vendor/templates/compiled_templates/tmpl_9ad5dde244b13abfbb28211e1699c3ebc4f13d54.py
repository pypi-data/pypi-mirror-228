from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'documentation/qos-profiles.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_qos_profiles = resolve('qos_profiles')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_3 = environment.filters['replace']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'replace' found.")
    try:
        t_4 = environment.filters['trim']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No filter named 'trim' found.")
    try:
        t_5 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_5(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_5((undefined(name='qos_profiles') if l_0_qos_profiles is missing else l_0_qos_profiles)):
        pass
        yield '\n### QOS Profiles\n\n#### QOS Profiles Summary\n\n'
        for l_1_profile in t_2((undefined(name='qos_profiles') if l_0_qos_profiles is missing else l_0_qos_profiles), 'name'):
            l_1_enabled = resolve('enabled')
            l_1_action = resolve('action')
            l_1_timeout = resolve('timeout')
            l_1_recovery = resolve('recovery')
            l_1_polling = resolve('polling')
            l_1_cos = l_1_dscp = l_1_trust = l_1_shape_rate = l_1_qos_sp = missing
            _loop_vars = {}
            pass
            yield '\nQOS Profile: **'
            yield str(environment.getattr(l_1_profile, 'name'))
            yield '**\n\n**Settings**\n\n| Default COS | Default DSCP | Trust | Shape Rate | QOS Service Policy |\n| ----------- | ------------ | ----- | ---------- | ------------------ |\n'
            l_1_cos = t_1(environment.getattr(l_1_profile, 'cos'), '-')
            _loop_vars['cos'] = l_1_cos
            l_1_dscp = t_1(environment.getattr(l_1_profile, 'dscp'), '-')
            _loop_vars['dscp'] = l_1_dscp
            l_1_trust = t_1(environment.getattr(l_1_profile, 'trust'), '-')
            _loop_vars['trust'] = l_1_trust
            l_1_shape_rate = t_1(environment.getattr(environment.getattr(l_1_profile, 'shape'), 'rate'), '-')
            _loop_vars['shape_rate'] = l_1_shape_rate
            l_1_qos_sp = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'service_policy'), 'type'), 'qos_input'), '-')
            _loop_vars['qos_sp'] = l_1_qos_sp
            yield '| '
            yield str((undefined(name='cos') if l_1_cos is missing else l_1_cos))
            yield ' | '
            yield str((undefined(name='dscp') if l_1_dscp is missing else l_1_dscp))
            yield ' | '
            yield str((undefined(name='trust') if l_1_trust is missing else l_1_trust))
            yield ' | '
            yield str((undefined(name='shape_rate') if l_1_shape_rate is missing else l_1_shape_rate))
            yield ' | '
            yield str((undefined(name='qos_sp') if l_1_qos_sp is missing else l_1_qos_sp))
            yield ' |\n'
            if ((t_5(environment.getattr(l_1_profile, 'tx_queues')) or t_5(environment.getattr(l_1_profile, 'uc_tx_queues'))) or t_5(environment.getattr(l_1_profile, 'mc_tx_queues'))):
                pass
                yield '\n**TX Queues**\n\n| TX queue | Type | Bandwidth | Priority | Shape Rate | Comment |\n| -------- | ---- | --------- | -------- | ---------- | ------- |\n'
                if t_5(environment.getattr(l_1_profile, 'tx_queues')):
                    pass
                    for l_2_tx_queue in t_2(environment.getattr(l_1_profile, 'tx_queues'), 'id'):
                        l_2_shape_rate = l_1_shape_rate
                        l_2_type = l_2_bw_percent = l_2_priority = l_2_comment = missing
                        _loop_vars = {}
                        pass
                        l_2_type = 'All'
                        _loop_vars['type'] = l_2_type
                        l_2_bw_percent = t_1(environment.getattr(l_2_tx_queue, 'bandwidth_percent'), environment.getattr(l_2_tx_queue, 'bandwidth_guaranteed_percent'), '-')
                        _loop_vars['bw_percent'] = l_2_bw_percent
                        l_2_priority = t_1(environment.getattr(l_2_tx_queue, 'priority'), '-')
                        _loop_vars['priority'] = l_2_priority
                        l_2_shape_rate = t_1(environment.getattr(environment.getattr(l_2_tx_queue, 'shape'), 'rate'), '-')
                        _loop_vars['shape_rate'] = l_2_shape_rate
                        l_2_comment = t_3(context.eval_ctx, t_4(t_1(environment.getattr(l_2_tx_queue, 'comment'), '-')), '\n', '<br>')
                        _loop_vars['comment'] = l_2_comment
                        yield '| '
                        yield str(environment.getattr(l_2_tx_queue, 'id'))
                        yield ' | '
                        yield str((undefined(name='type') if l_2_type is missing else l_2_type))
                        yield ' | '
                        yield str((undefined(name='bw_percent') if l_2_bw_percent is missing else l_2_bw_percent))
                        yield ' | '
                        yield str((undefined(name='priority') if l_2_priority is missing else l_2_priority))
                        yield ' | '
                        yield str((undefined(name='shape_rate') if l_2_shape_rate is missing else l_2_shape_rate))
                        yield ' | '
                        yield str((undefined(name='comment') if l_2_comment is missing else l_2_comment))
                        yield ' |\n'
                    l_2_tx_queue = l_2_type = l_2_bw_percent = l_2_priority = l_2_shape_rate = l_2_comment = missing
                if t_5(environment.getattr(l_1_profile, 'uc_tx_queues')):
                    pass
                    for l_2_uc_tx_queue in t_2(environment.getattr(l_1_profile, 'uc_tx_queues'), 'id'):
                        l_2_shape_rate = l_1_shape_rate
                        l_2_type = l_2_bw_percent = l_2_priority = l_2_comment = missing
                        _loop_vars = {}
                        pass
                        l_2_type = 'Unicast'
                        _loop_vars['type'] = l_2_type
                        l_2_bw_percent = t_1(environment.getattr(l_2_uc_tx_queue, 'bandwidth_percent'), environment.getattr(l_2_uc_tx_queue, 'bandwidth_guaranteed_percent'), '-')
                        _loop_vars['bw_percent'] = l_2_bw_percent
                        l_2_priority = t_1(environment.getattr(l_2_uc_tx_queue, 'priority'), '-')
                        _loop_vars['priority'] = l_2_priority
                        l_2_shape_rate = t_1(environment.getattr(environment.getattr(l_2_uc_tx_queue, 'shape'), 'rate'), '-')
                        _loop_vars['shape_rate'] = l_2_shape_rate
                        l_2_comment = t_3(context.eval_ctx, t_4(t_1(environment.getattr(l_2_uc_tx_queue, 'comment'), '-')), '\n', '<br>')
                        _loop_vars['comment'] = l_2_comment
                        yield '| '
                        yield str(environment.getattr(l_2_uc_tx_queue, 'id'))
                        yield ' | '
                        yield str((undefined(name='type') if l_2_type is missing else l_2_type))
                        yield ' | '
                        yield str((undefined(name='bw_percent') if l_2_bw_percent is missing else l_2_bw_percent))
                        yield ' | '
                        yield str((undefined(name='priority') if l_2_priority is missing else l_2_priority))
                        yield ' | '
                        yield str((undefined(name='shape_rate') if l_2_shape_rate is missing else l_2_shape_rate))
                        yield ' | '
                        yield str((undefined(name='comment') if l_2_comment is missing else l_2_comment))
                        yield ' |\n'
                    l_2_uc_tx_queue = l_2_type = l_2_bw_percent = l_2_priority = l_2_shape_rate = l_2_comment = missing
                if t_5(environment.getattr(l_1_profile, 'mc_tx_queues')):
                    pass
                    for l_2_mc_tx_queue in t_2(environment.getattr(l_1_profile, 'mc_tx_queues'), 'id'):
                        l_2_shape_rate = l_1_shape_rate
                        l_2_type = l_2_bw_percent = l_2_priority = l_2_comment = missing
                        _loop_vars = {}
                        pass
                        l_2_type = 'Multicast'
                        _loop_vars['type'] = l_2_type
                        l_2_bw_percent = t_1(environment.getattr(l_2_mc_tx_queue, 'bandwidth_percent'), environment.getattr(l_2_mc_tx_queue, 'bandwidth_guaranteed_percent'), '-')
                        _loop_vars['bw_percent'] = l_2_bw_percent
                        l_2_priority = t_1(environment.getattr(l_2_mc_tx_queue, 'priority'), '-')
                        _loop_vars['priority'] = l_2_priority
                        l_2_shape_rate = t_1(environment.getattr(environment.getattr(l_2_mc_tx_queue, 'shape'), 'rate'), '-')
                        _loop_vars['shape_rate'] = l_2_shape_rate
                        l_2_comment = t_3(context.eval_ctx, t_4(t_1(environment.getattr(l_2_mc_tx_queue, 'comment'), '-')), '\n', '<br>')
                        _loop_vars['comment'] = l_2_comment
                        yield '| '
                        yield str(environment.getattr(l_2_mc_tx_queue, 'id'))
                        yield ' | '
                        yield str((undefined(name='type') if l_2_type is missing else l_2_type))
                        yield ' | '
                        yield str((undefined(name='bw_percent') if l_2_bw_percent is missing else l_2_bw_percent))
                        yield ' | '
                        yield str((undefined(name='priority') if l_2_priority is missing else l_2_priority))
                        yield ' | '
                        yield str((undefined(name='shape_rate') if l_2_shape_rate is missing else l_2_shape_rate))
                        yield ' | '
                        yield str((undefined(name='comment') if l_2_comment is missing else l_2_comment))
                        yield ' |\n'
                    l_2_mc_tx_queue = l_2_type = l_2_bw_percent = l_2_priority = l_2_shape_rate = l_2_comment = missing
            if t_5(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'enabled'), True):
                pass
                yield '\n**Priority Flow Control**\n\nPriority Flow Control is **enabled**.\n\n| Priority | Action |\n| -------- | ------ |\n'
                for l_2_priority_block in t_2(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'priorities'), 'priority'):
                    l_2_action = l_1_action
                    _loop_vars = {}
                    pass
                    if t_5(environment.getattr(l_2_priority_block, 'priority')):
                        pass
                        if t_5(environment.getattr(l_2_priority_block, 'no_drop'), True):
                            pass
                            l_2_action = 'no-drop'
                            _loop_vars['action'] = l_2_action
                        else:
                            pass
                            l_2_action = 'drop'
                            _loop_vars['action'] = l_2_action
                        yield '| '
                        yield str(environment.getattr(l_2_priority_block, 'priority'))
                        yield ' | '
                        yield str((undefined(name='action') if l_2_action is missing else l_2_action))
                        yield ' |\n'
                l_2_priority_block = l_2_action = missing
                if t_5(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'watchdog'), 'enabled'), True):
                    pass
                    l_1_enabled = environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'watchdog'), 'enabled')
                    _loop_vars['enabled'] = l_1_enabled
                    l_1_action = t_1(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'watchdog'), 'action'), 'errdisable')
                    _loop_vars['action'] = l_1_action
                    l_1_timeout = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'watchdog'), 'timer'), 'timeout'), '-')
                    _loop_vars['timeout'] = l_1_timeout
                    l_1_recovery = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'watchdog'), 'timer'), 'recovery_time'), '-')
                    _loop_vars['recovery'] = l_1_recovery
                    l_1_polling = t_1(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_profile, 'priority_flow_control'), 'watchdog'), 'timer'), 'polling_interval'), '-')
                    _loop_vars['polling'] = l_1_polling
                    yield '\n**Priority Flow Control watchdog settings**\n\n| Enabled | Action | Timeout | Recovery | Polling |\n| ------- | ------ | ------- | -------- | ------- |\n| '
                    yield str((undefined(name='enabled') if l_1_enabled is missing else l_1_enabled))
                    yield ' | '
                    yield str((undefined(name='action') if l_1_action is missing else l_1_action))
                    yield ' | '
                    yield str((undefined(name='timeout') if l_1_timeout is missing else l_1_timeout))
                    yield ' | '
                    yield str((undefined(name='recovery') if l_1_recovery is missing else l_1_recovery))
                    yield ' | '
                    yield str((undefined(name='polling') if l_1_polling is missing else l_1_polling))
                    yield ' |\n'
        l_1_profile = l_1_cos = l_1_dscp = l_1_trust = l_1_shape_rate = l_1_qos_sp = l_1_enabled = l_1_action = l_1_timeout = l_1_recovery = l_1_polling = missing
        yield '\n#### QOS Profile Device Configuration\n\n```eos\n'
        template = environment.get_template('eos/qos-profiles.j2', 'documentation/qos-profiles.j2')
        for event in template.root_render_func(template.new_context(context.get_all(), True, {})):
            yield event
        yield '```\n'

blocks = {}
debug_info = '7=42&13=45&15=55&21=57&22=59&23=61&24=63&25=65&26=68&27=78&35=81&36=83&37=88&38=90&41=92&42=94&43=96&44=99&47=112&48=114&49=119&50=121&53=123&54=125&55=127&56=130&59=143&60=145&61=150&62=152&65=154&66=156&67=158&68=161&72=174&80=177&81=181&82=183&83=185&85=189&87=192&90=197&91=199&92=201&93=203&94=205&95=207&101=210&109=222'