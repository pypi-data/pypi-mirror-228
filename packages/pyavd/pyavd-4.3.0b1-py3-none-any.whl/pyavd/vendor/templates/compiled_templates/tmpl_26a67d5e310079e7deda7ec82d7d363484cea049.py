from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/ip-client-source-interfaces.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ip_ftp_client_source_interfaces = resolve('ip_ftp_client_source_interfaces')
    l_0_ip_http_client_source_interface = resolve('ip_http_client_source_interface')
    l_0_ip_ssh_client_source_interfaces = resolve('ip_ssh_client_source_interfaces')
    l_0_ip_telnet_client_source_interfaces = resolve('ip_telnet_client_source_interfaces')
    l_0_ip_tftp_client_source_interfaces = resolve('ip_tftp_client_source_interfaces')
    l_0_ip_http_client_source_interfaces = resolve('ip_http_client_source_interfaces')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.filters['capitalize']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'capitalize' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if ((((t_3((undefined(name='ip_ftp_client_source_interfaces') if l_0_ip_ftp_client_source_interfaces is missing else l_0_ip_ftp_client_source_interfaces)) or t_3((undefined(name='ip_http_client_source_interface') if l_0_ip_http_client_source_interface is missing else l_0_ip_http_client_source_interface))) or t_3((undefined(name='ip_ssh_client_source_interfaces') if l_0_ip_ssh_client_source_interfaces is missing else l_0_ip_ssh_client_source_interfaces))) or t_3((undefined(name='ip_telnet_client_source_interfaces') if l_0_ip_telnet_client_source_interfaces is missing else l_0_ip_telnet_client_source_interfaces))) or t_3((undefined(name='ip_tftp_client_source_interfaces') if l_0_ip_tftp_client_source_interfaces is missing else l_0_ip_tftp_client_source_interfaces))):
        pass
        yield '!\n'
        if t_3((undefined(name='ip_ftp_client_source_interfaces') if l_0_ip_ftp_client_source_interfaces is missing else l_0_ip_ftp_client_source_interfaces)):
            pass
            for l_1_ip_ftp_client_source_interface in (undefined(name='ip_ftp_client_source_interfaces') if l_0_ip_ftp_client_source_interfaces is missing else l_0_ip_ftp_client_source_interfaces):
                l_1_ip_ftp_client_cli = resolve('ip_ftp_client_cli')
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_1_ip_ftp_client_source_interface, 'name')):
                    pass
                    l_1_ip_ftp_client_cli = str_join(('ip ftp client source-interface ', t_2(environment.getattr(l_1_ip_ftp_client_source_interface, 'name')), ))
                    _loop_vars['ip_ftp_client_cli'] = l_1_ip_ftp_client_cli
                    if t_3(environment.getattr(l_1_ip_ftp_client_source_interface, 'vrf')):
                        pass
                        l_1_ip_ftp_client_cli = str_join(((undefined(name='ip_ftp_client_cli') if l_1_ip_ftp_client_cli is missing else l_1_ip_ftp_client_cli), ' vrf ', environment.getattr(l_1_ip_ftp_client_source_interface, 'vrf'), ))
                        _loop_vars['ip_ftp_client_cli'] = l_1_ip_ftp_client_cli
                    yield str((undefined(name='ip_ftp_client_cli') if l_1_ip_ftp_client_cli is missing else l_1_ip_ftp_client_cli))
                    yield '\n'
            l_1_ip_ftp_client_source_interface = l_1_ip_ftp_client_cli = missing
        for l_1_ip_http_client_source_interface in t_1((undefined(name='ip_http_client_source_interfaces') if l_0_ip_http_client_source_interfaces is missing else l_0_ip_http_client_source_interfaces)):
            l_1_ip_http_client_cli = missing
            _loop_vars = {}
            pass
            l_1_ip_http_client_cli = 'ip http client'
            _loop_vars['ip_http_client_cli'] = l_1_ip_http_client_cli
            if t_3(environment.getattr(l_1_ip_http_client_source_interface, 'name')):
                pass
                l_1_ip_http_client_cli = str_join(((undefined(name='ip_http_client_cli') if l_1_ip_http_client_cli is missing else l_1_ip_http_client_cli), ' local-interface ', environment.getattr(l_1_ip_http_client_source_interface, 'name'), ))
                _loop_vars['ip_http_client_cli'] = l_1_ip_http_client_cli
                if t_3(environment.getattr(l_1_ip_http_client_source_interface, 'vrf')):
                    pass
                    l_1_ip_http_client_cli = str_join(((undefined(name='ip_http_client_cli') if l_1_ip_http_client_cli is missing else l_1_ip_http_client_cli), ' vrf ', environment.getattr(l_1_ip_http_client_source_interface, 'vrf'), ))
                    _loop_vars['ip_http_client_cli'] = l_1_ip_http_client_cli
                yield str((undefined(name='ip_http_client_cli') if l_1_ip_http_client_cli is missing else l_1_ip_http_client_cli))
                yield '\n'
        l_1_ip_http_client_source_interface = l_1_ip_http_client_cli = missing
        if t_3((undefined(name='ip_ssh_client_source_interfaces') if l_0_ip_ssh_client_source_interfaces is missing else l_0_ip_ssh_client_source_interfaces)):
            pass
            for l_1_ip_ssh_client_source_interface in t_1((undefined(name='ip_ssh_client_source_interfaces') if l_0_ip_ssh_client_source_interfaces is missing else l_0_ip_ssh_client_source_interfaces)):
                l_1_ip_ssh_client_cli = resolve('ip_ssh_client_cli')
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_1_ip_ssh_client_source_interface, 'name')):
                    pass
                    l_1_ip_ssh_client_cli = str_join(('ip ssh client source-interface ', t_2(environment.getattr(l_1_ip_ssh_client_source_interface, 'name')), ))
                    _loop_vars['ip_ssh_client_cli'] = l_1_ip_ssh_client_cli
                    if t_3(environment.getattr(l_1_ip_ssh_client_source_interface, 'vrf')):
                        pass
                        l_1_ip_ssh_client_cli = str_join(((undefined(name='ip_ssh_client_cli') if l_1_ip_ssh_client_cli is missing else l_1_ip_ssh_client_cli), ' vrf ', environment.getattr(l_1_ip_ssh_client_source_interface, 'vrf'), ))
                        _loop_vars['ip_ssh_client_cli'] = l_1_ip_ssh_client_cli
                    yield str((undefined(name='ip_ssh_client_cli') if l_1_ip_ssh_client_cli is missing else l_1_ip_ssh_client_cli))
                    yield '\n'
            l_1_ip_ssh_client_source_interface = l_1_ip_ssh_client_cli = missing
        if t_3((undefined(name='ip_telnet_client_source_interfaces') if l_0_ip_telnet_client_source_interfaces is missing else l_0_ip_telnet_client_source_interfaces)):
            pass
            for l_1_ip_telnet_client_source_interface in (undefined(name='ip_telnet_client_source_interfaces') if l_0_ip_telnet_client_source_interfaces is missing else l_0_ip_telnet_client_source_interfaces):
                l_1_ip_telnet_client_cli = resolve('ip_telnet_client_cli')
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_1_ip_telnet_client_source_interface, 'name')):
                    pass
                    l_1_ip_telnet_client_cli = str_join(('ip telnet client source-interface ', t_2(environment.getattr(l_1_ip_telnet_client_source_interface, 'name')), ))
                    _loop_vars['ip_telnet_client_cli'] = l_1_ip_telnet_client_cli
                    if t_3(environment.getattr(l_1_ip_telnet_client_source_interface, 'vrf')):
                        pass
                        l_1_ip_telnet_client_cli = str_join(((undefined(name='ip_telnet_client_cli') if l_1_ip_telnet_client_cli is missing else l_1_ip_telnet_client_cli), ' vrf ', environment.getattr(l_1_ip_telnet_client_source_interface, 'vrf'), ))
                        _loop_vars['ip_telnet_client_cli'] = l_1_ip_telnet_client_cli
                    yield str((undefined(name='ip_telnet_client_cli') if l_1_ip_telnet_client_cli is missing else l_1_ip_telnet_client_cli))
                    yield '\n'
            l_1_ip_telnet_client_source_interface = l_1_ip_telnet_client_cli = missing
        if t_3((undefined(name='ip_tftp_client_source_interfaces') if l_0_ip_tftp_client_source_interfaces is missing else l_0_ip_tftp_client_source_interfaces)):
            pass
            for l_1_ip_tftp_client_source_interface in (undefined(name='ip_tftp_client_source_interfaces') if l_0_ip_tftp_client_source_interfaces is missing else l_0_ip_tftp_client_source_interfaces):
                l_1_ip_tftp_client_cli = resolve('ip_tftp_client_cli')
                _loop_vars = {}
                pass
                if t_3(environment.getattr(l_1_ip_tftp_client_source_interface, 'name')):
                    pass
                    l_1_ip_tftp_client_cli = str_join(('ip tftp client source-interface ', t_2(environment.getattr(l_1_ip_tftp_client_source_interface, 'name')), ))
                    _loop_vars['ip_tftp_client_cli'] = l_1_ip_tftp_client_cli
                    if t_3(environment.getattr(l_1_ip_tftp_client_source_interface, 'vrf')):
                        pass
                        l_1_ip_tftp_client_cli = str_join(((undefined(name='ip_tftp_client_cli') if l_1_ip_tftp_client_cli is missing else l_1_ip_tftp_client_cli), ' vrf ', environment.getattr(l_1_ip_tftp_client_source_interface, 'vrf'), ))
                        _loop_vars['ip_tftp_client_cli'] = l_1_ip_tftp_client_cli
                    yield str((undefined(name='ip_tftp_client_cli') if l_1_ip_tftp_client_cli is missing else l_1_ip_tftp_client_cli))
                    yield '\n'
            l_1_ip_tftp_client_source_interface = l_1_ip_tftp_client_cli = missing

blocks = {}
debug_info = '7=35&13=38&14=40&15=44&16=46&17=48&18=50&20=52&24=55&25=59&26=61&27=63&28=65&29=67&31=69&34=72&35=74&36=78&37=80&38=82&39=84&41=86&45=89&46=91&47=95&48=97&49=99&50=101&52=103&56=106&57=108&58=112&59=114&60=116&61=118&63=120'