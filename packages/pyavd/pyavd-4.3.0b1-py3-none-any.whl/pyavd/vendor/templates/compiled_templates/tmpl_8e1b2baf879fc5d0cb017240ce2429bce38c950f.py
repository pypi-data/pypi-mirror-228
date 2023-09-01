from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/ip-access-lists.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_ip_access_lists = resolve('ip_access_lists')
    l_0_namespace = resolve('namespace')
    l_0_counter = resolve('counter')
    try:
        t_1 = environment.filters['arista.avd.default']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.default' found.")
    try:
        t_2 = environment.filters['lower']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'lower' found.")
    try:
        t_3 = environment.filters['mandatory']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No filter named 'mandatory' found.")
    try:
        t_4 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    pass
    if t_4((undefined(name='ip_access_lists') if l_0_ip_access_lists is missing else l_0_ip_access_lists)):
        pass
        l_0_counter = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace))
        context.vars['counter'] = l_0_counter
        context.exported_vars.add('counter')
        if not isinstance(l_0_counter, Namespace):
            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
        l_0_counter['acle_number'] = 0
        for l_1_acl in (undefined(name='ip_access_lists') if l_0_ip_access_lists is missing else l_0_ip_access_lists):
            _loop_vars = {}
            pass
            if ((not t_4(environment.getattr(l_1_acl, 'name'))) or (not t_4(environment.getattr(l_1_acl, 'entries')))):
                pass
                continue
            yield 'ip access-list '
            yield str(environment.getattr(l_1_acl, 'name'))
            yield '\n'
            if t_4(environment.getattr(l_1_acl, 'counters_per_entry'), True):
                pass
                yield '   counters per-entry\n'
            for l_2_acle in environment.getattr(l_1_acl, 'entries'):
                l_2_ip_access_lists_max_entries = resolve('ip_access_lists_max_entries')
                l_2_a_non_existing_var = resolve('a_non_existing_var')
                l_2_acl_entry = missing
                _loop_vars = {}
                pass
                l_2_acl_entry = context.call((undefined(name='namespace') if l_0_namespace is missing else l_0_namespace), string='', _loop_vars=_loop_vars)
                _loop_vars['acl_entry'] = l_2_acl_entry
                if t_4(environment.getattr(l_2_acle, 'sequence')):
                    pass
                    if not isinstance(l_2_acl_entry, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), environment.getattr(l_2_acle, 'sequence'), ' ', ))
                if t_4(environment.getattr(l_2_acle, 'remark')):
                    pass
                    if not isinstance(l_2_acl_entry, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), 'remark ', environment.getattr(l_2_acle, 'remark'), ))
                elif (((t_4(environment.getattr(l_2_acle, 'action')) and t_4(environment.getattr(l_2_acle, 'protocol'))) and t_4(environment.getattr(l_2_acle, 'source'))) and t_4(environment.getattr(l_2_acle, 'destination'))):
                    pass
                    if not isinstance(l_2_acl_entry, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), environment.getattr(l_2_acle, 'action'), ))
                    if (t_4(environment.getattr(l_2_acle, 'vlan_number')) and t_4(environment.getattr(l_2_acle, 'vlan_mask'))):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' vlan', ))
                        if t_4(environment.getattr(l_2_acle, 'vlan_inner'), True):
                            pass
                            if not isinstance(l_2_acl_entry, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' inner', ))
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', environment.getattr(l_2_acle, 'vlan_number'), ' ', environment.getattr(l_2_acle, 'vlan_mask'), ))
                    if not isinstance(l_2_acl_entry, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', environment.getattr(l_2_acle, 'protocol'), ))
                    if (('/' not in environment.getattr(l_2_acle, 'source')) and (environment.getattr(l_2_acle, 'source') != 'any')):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' host', ))
                    if not isinstance(l_2_acl_entry, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', environment.getattr(l_2_acle, 'source'), ))
                    if (t_2(environment.getattr(l_2_acle, 'protocol')) in ['tcp', 'udp']):
                        pass
                        if t_4(environment.getattr(l_2_acle, 'source_ports')):
                            pass
                            if not isinstance(l_2_acl_entry, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', t_1(environment.getattr(l_2_acle, 'source_ports_match'), 'eq'), ))
                            for l_3_a_port in environment.getattr(l_2_acle, 'source_ports'):
                                _loop_vars = {}
                                pass
                                if not isinstance(l_2_acl_entry, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', l_3_a_port, ))
                            l_3_a_port = missing
                    if (('/' not in environment.getattr(l_2_acle, 'destination')) and (environment.getattr(l_2_acle, 'destination') != 'any')):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' host', ))
                    if not isinstance(l_2_acl_entry, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', environment.getattr(l_2_acle, 'destination'), ))
                    if (t_2(environment.getattr(l_2_acle, 'protocol')) in ['tcp', 'udp']):
                        pass
                        if t_4(environment.getattr(l_2_acle, 'destination_ports')):
                            pass
                            if not isinstance(l_2_acl_entry, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', t_1(environment.getattr(l_2_acle, 'destination_ports_match'), 'eq'), ))
                            for l_3_a_port in environment.getattr(l_2_acle, 'destination_ports'):
                                _loop_vars = {}
                                pass
                                if not isinstance(l_2_acl_entry, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', l_3_a_port, ))
                            l_3_a_port = missing
                    if (t_2(environment.getattr(l_2_acle, 'protocol')) == 'tcp'):
                        pass
                        if t_4(environment.getattr(l_2_acle, 'tcp_flags')):
                            pass
                            for l_3_a_flag in environment.getattr(l_2_acle, 'tcp_flags'):
                                _loop_vars = {}
                                pass
                                if not isinstance(l_2_acl_entry, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', l_3_a_flag, ))
                            l_3_a_flag = missing
                    if (t_2(environment.getattr(l_2_acle, 'protocol')) == 'icmp'):
                        pass
                        if t_4(environment.getattr(l_2_acle, 'icmp_type')):
                            pass
                            if not isinstance(l_2_acl_entry, Namespace):
                                raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                            l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', environment.getattr(l_2_acle, 'icmp_type'), ))
                            if t_4(environment.getattr(l_2_acle, 'icmp_code')):
                                pass
                                if not isinstance(l_2_acl_entry, Namespace):
                                    raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                                l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', environment.getattr(l_2_acle, 'icmp_code'), ))
                    if t_4(environment.getattr(l_2_acle, 'nexthop_group')):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' nexthop-group ', environment.getattr(l_2_acle, 'nexthop_group'), ))
                    if t_4(environment.getattr(l_2_acle, 'fragments'), True):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' fragments', ))
                    if t_4(environment.getattr(l_2_acle, 'tracked'), True):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' tracked', ))
                    if t_4(environment.getattr(l_2_acle, 'ttl')):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ttl ', t_1(environment.getattr(l_2_acle, 'ttl_match'), 'eq'), ))
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' ', environment.getattr(l_2_acle, 'ttl'), ))
                    if t_4(environment.getattr(l_2_acle, 'dscp')):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' dscp ', t_2(environment.getattr(l_2_acle, 'dscp')), ))
                    if t_4(environment.getattr(l_2_acle, 'log'), True):
                        pass
                        if not isinstance(l_2_acl_entry, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_2_acl_entry['string'] = str_join((environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'), ' log', ))
                    if t_4((undefined(name='ip_access_lists_max_entries') if l_2_ip_access_lists_max_entries is missing else l_2_ip_access_lists_max_entries)):
                        pass
                        if not isinstance(l_0_counter, Namespace):
                            raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                        l_0_counter['acle_number'] = (environment.getattr((undefined(name='counter') if l_0_counter is missing else l_0_counter), 'acle_number') + 1)
                        if (environment.getattr((undefined(name='counter') if l_0_counter is missing else l_0_counter), 'acle_number') > (undefined(name='ip_access_lists_max_entries') if l_2_ip_access_lists_max_entries is missing else l_2_ip_access_lists_max_entries)):
                            pass
                            yield '   '
                            yield str(t_3((undefined(name='a_non_existing_var') if l_2_a_non_existing_var is missing else l_2_a_non_existing_var), 'The number of ACL entries is above defined maximum!'))
                            yield '\n'
                yield '   '
                yield str(environment.getattr((undefined(name='acl_entry') if l_2_acl_entry is missing else l_2_acl_entry), 'string'))
                yield '\n'
            l_2_acle = l_2_acl_entry = l_2_ip_access_lists_max_entries = l_2_a_non_existing_var = missing
        l_1_acl = missing

blocks = {}
debug_info = '7=38&9=40&10=43&12=46&13=49&16=51&18=53&19=55&23=58&26=64&28=66&29=68&33=71&34=73&37=76&42=78&44=81&45=83&46=86&47=88&49=91&52=94&54=97&55=99&57=102&59=105&60=107&61=109&62=112&63=115&68=119&69=121&71=124&73=127&74=129&75=131&76=134&77=137&82=141&83=143&84=145&85=148&90=152&91=154&92=156&93=159&94=161&99=164&100=166&103=169&104=171&107=174&108=176&111=179&112=181&113=184&116=187&117=189&120=192&121=194&124=197&125=199&126=202&128=205&132=208'