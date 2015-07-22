import logging


log = logging.getLogger(__name__)


def up(config, project=None, cmd="docker-compose", pull=True, env={}):
    """
    runs `docker-compose up -d --x-smart-recreate`
    if docker-compose complains that one needs to migrate from configs to tags
    then it will run `docker-compose migrate-to-labels`
    and rerun `docker-compose up -d --x-smart-recreate`
    :param config: path to docker-compose.yml file
    :param project: project name
    :param cmd: path to docker-compose executable
    :return:
    """
    result = True
    changes = {}
    comment = []

    if project:
        project_option = "-p {}".format(project)
    else:
        project_option = ""

    # let's try pulling
    if pull:
        cmd_line = "{cmd} -f {config} {project_option} pull".format(cmd=cmd, config=config, project_option=project_option)
        log.info("executing docker-compose pull")
        fig_res = __salt__['cmd.run_all']("{} ".format(cmd_line), env=env)
        if fig_res['retcode']:
            result = False
            changes.update(fig_res)
            return result, changes, "Error running {}".format(cmd_line)

    # let's try up
    cmd_line = "{cmd} -f {config} {project_option} up -d --x-smart-recreate".format(cmd=cmd, config=config, project_option=project_option)
    log.info("executing docker-compose up")

    fig_res = __salt__['cmd.run_all']("{} ".format(cmd_line), env=env)
    fig_output = fig_res['stderr'] + fig_res['stdout']

    # in case compose recommended to run migrate-to-labels
    if fig_res['retcode'] and 'migrate-to-labels' in fig_output:
        log.info("Falling back to migrate-to-labels")
        log.info("Executing docker-compose migrate-to-label")
        cmd_line = "{cmd} -f {config} {project_option} migrate-to-labels".format(cmd=cmd, config=config, project_option=project_option, env=env)
        fig_res = __salt__['cmd.run_all']("{} ".format(cmd_line))
        fig_output = fig_res['stderr'] + fig_res['stdout']

    if fig_res['retcode']:
        result = False
        changes.update(fig_res)
        return result, changes, "Error running {}".format(cmd_line)

    # let's update changes dictionary for salt to pick up changes
    if fig_output:
        for line in fig_output.splitlines():
            line = line.strip()
            if line.startswith("Starting "):
                if 'started' not in changes:
                    changes['started']  = []
                changes['started'].append(line)
            elif line.startswith("Creating "):
                if 'created' not in changes:
                    changes['created'] = []
                changes['created'].append(line)
            elif line.startswith("Recreating "):
                if 'recreated' not in changes:
                    changes['recreated'] = []
                changes['recreated'].append(line)
            elif line.endswith(" up-to-date"):
                comment.append(line)
            else:
                comment.append(line)


    # just appending stderr to comment as error code is not set so this might be a warning
    if fig_res['stderr']:
        for line in fig_res['stderr'].splitlines():
            comment.append(line)

    return result, changes, reduce(lambda x, y: x + y, comment)


def cmd(config, project=None, arg='', cmd="docker-compose"):
    if project:
        project_option = "-p {}".format(project)
    else:
        project_option = ""

    cmd_line = "{cmd} -f {config} {project_option} {arg}".format(cmd=cmd, config=config, project_option=project_option, arg=arg)
    return __salt__['cmd.run_all']("{} ".format(cmd_line))
