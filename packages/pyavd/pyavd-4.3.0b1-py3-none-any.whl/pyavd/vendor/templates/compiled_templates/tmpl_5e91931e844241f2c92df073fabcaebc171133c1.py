from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/flow-trackings.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_flow_trackings = resolve('flow_trackings')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    for l_1_flow_tracking in t_1((undefined(name='flow_trackings') if l_0_flow_trackings is missing else l_0_flow_trackings), []):
        _loop_vars = {}
        pass
        yield '!\nflow tracking '
        yield str(environment.getattr(l_1_flow_tracking, 'type'))
        yield '\n'
        if t_2(environment.getattr(l_1_flow_tracking, 'sample')):
            pass
            yield '   sample '
            yield str(environment.getattr(l_1_flow_tracking, 'sample'))
            yield '\n'
        for l_2_tracker in environment.getattr(l_1_flow_tracking, 'trackers'):
            _loop_vars = {}
            pass
            yield '   tracker '
            yield str(environment.getattr(l_2_tracker, 'name'))
            yield '\n'
            if t_2(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'on_inactive_timeout')):
                pass
                yield '      record export on inactive timeout '
                yield str(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'on_inactive_timeout'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'on_interval')):
                pass
                yield '      record export on interval '
                yield str(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'on_interval'))
                yield '\n'
            if t_2(environment.getattr(environment.getattr(l_2_tracker, 'record_export'), 'mpls'), True):
                pass
                yield '      record export mpls\n'
            if t_2(environment.getattr(l_2_tracker, 'exporters')):
                pass
                for l_3_exporter in environment.getattr(l_2_tracker, 'exporters'):
                    l_3_collector_cli = resolve('collector_cli')
                    _loop_vars = {}
                    pass
                    yield '      exporter '
                    yield str(environment.getattr(l_3_exporter, 'name'))
                    yield '\n'
                    if t_2(environment.getattr(environment.getattr(l_3_exporter, 'collector'), 'host')):
                        pass
                        l_3_collector_cli = str_join(('collector ', environment.getattr(environment.getattr(l_3_exporter, 'collector'), 'host'), ))
                        _loop_vars['collector_cli'] = l_3_collector_cli
                        if t_2(environment.getattr(environment.getattr(l_3_exporter, 'collector'), 'port')):
                            pass
                            l_3_collector_cli = str_join(((undefined(name='collector_cli') if l_3_collector_cli is missing else l_3_collector_cli), ' port ', environment.getattr(environment.getattr(l_3_exporter, 'collector'), 'port'), ))
                            _loop_vars['collector_cli'] = l_3_collector_cli
                        yield '         '
                        yield str((undefined(name='collector_cli') if l_3_collector_cli is missing else l_3_collector_cli))
                        yield '\n'
                    if t_2(environment.getattr(environment.getattr(l_3_exporter, 'format'), 'ipfix_version')):
                        pass
                        yield '         format ipfix version '
                        yield str(environment.getattr(environment.getattr(l_3_exporter, 'format'), 'ipfix_version'))
                        yield '\n'
                    if t_2(environment.getattr(l_3_exporter, 'local_interface')):
                        pass
                        yield '         local interface '
                        yield str(environment.getattr(l_3_exporter, 'local_interface'))
                        yield '\n'
                    if t_2(environment.getattr(l_3_exporter, 'template_interval')):
                        pass
                        yield '         template interval '
                        yield str(environment.getattr(l_3_exporter, 'template_interval'))
                        yield '\n'
                l_3_exporter = l_3_collector_cli = missing
            if t_2(environment.getattr(l_2_tracker, 'table_size')):
                pass
                yield '      flow table size '
                yield str(environment.getattr(l_2_tracker, 'table_size'))
                yield ' entries\n'
        l_2_tracker = missing
        if t_2(environment.getattr(l_1_flow_tracking, 'shutdown'), False):
            pass
            yield '   no shutdown\n'
    l_1_flow_tracking = missing

blocks = {}
debug_info = '7=24&9=28&10=30&11=33&13=35&14=39&15=41&16=44&18=46&19=49&21=51&24=54&25=56&26=61&27=63&28=65&29=67&30=69&32=72&34=74&35=77&37=79&38=82&40=84&41=87&45=90&46=93&49=96'