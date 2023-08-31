from argparse import ArgumentParser
from zetsubou.commands.base_command import Command
from zetsubou.commands.command_context import CommandContext
from zetsubou.commands.generate import Generate
from zetsubou.commands.install import Install
from zetsubou.fastbuild.fastbuild_emit import FastbuildEmitter
from zetsubou.project.model.config_string import EDefaultConfigSlots
from zetsubou.project.model.kind import ETargetKind
from zetsubou.project.runtime.emit import EDefaultTargets, EmitContext
from zetsubou.project.runtime.project_loader import ProjectTemplate
from zetsubou.utils import logger
from zetsubou.utils.common import null_or_empty
from zetsubou.utils.error import CompilationError, ProjectError
from zetsubou.utils.subprocess import call_process_venv


class Build(Command):
    @property
    def name(self):
        return 'build'

    @property
    def desc(self):
        return 'Builds specified target for specified or all configs. Triggers Install and Generate if user changes were detected since last run.'

    @property
    def help(self):
        return self.desc

    def ParseArgs(self, arg_parser: ArgumentParser):
        config_or_variant = arg_parser.add_mutually_exclusive_group()

        config_or_variant.add_argument('--config', help='Builds all targets using this specific config')
        config_or_variant.add_argument('--target', help='Builds all configs for this specific target')
        config_or_variant.add_argument('--target-variant', help='Builds only this specific target variant')

    @property
    def needs_project_loaded(self):
        return True

    def pick_variants(self, context: CommandContext, arg_config:str):
        config_variants = []

        if not null_or_empty(arg_config):
            proj_config = context.project_template.find_config(arg_config)
            if proj_config is None:
                logger.Error(f"Unknown config '{arg_config}'")

            config_variants = context.config_matrix.find_variants({ 'configuration' : proj_config.configuration })

        else:
            config_variants = context.config_matrix.variants

        return config_variants

    def pick_target(self, context:CommandContext, arg_target:str) -> str:
        if null_or_empty(arg_target) or arg_target == EDefaultTargets.All.name:
            return EDefaultTargets.All.name

        build_target = context.project_template.find_target(arg_target)
        if build_target is None:
            raise ProjectError(f"Unknown target '{arg_target}'")

        return context.project_template.compile_target_variant_name(build_target.config.kind, build_target.target)

    def OnExecute(self, context: CommandContext):
        if context.file_cache.is_stale():
            Command.get_command_instance(Install).Execute(context)
            Command.get_command_instance(Generate).Execute(context)
        else:
            # Already done by the above, if cache is fresh, we just find the venv
            context.resolve_venv()

        try:
            arg_target = context.command_args.target
            arg_config = context.command_args.config
            arg_variant = context.command_args.target_variant

            target_variants = []

            if not null_or_empty(arg_variant):
                target_and_kind, config = ProjectTemplate.decompose_variant_name(arg_variant, context.project_template.project.config.config_string)
                if target_and_kind is None or config is None:
                    raise ProjectError(f"Unable to parse target variant string '{arg_variant}'")

                # TODO make this more robust
                target_parts = target_and_kind.split('_')
                if len(target_parts) > 2:
                    kind = f"{target_parts[1]}_{target_parts[2]}"
                    if not any(filter(lambda e : kind.startswith(e[0]), ETargetKind.__members__)):
                        raise ProjectError(f"Unknown target kind '{kind}'")

                target = target_parts[0]

                if not context.project_template.find_target(target) and target != EDefaultTargets.All.name:
                    raise ProjectError(f"Unknown target '{target}'")

                if not context.project_template.find_config(config[EDefaultConfigSlots.configuration.name]):
                    raise ProjectError(f"Unknown configuration '{config[EDefaultConfigSlots.configuration.name]}'")

                if not context.project_template.find_platform(config[EDefaultConfigSlots.platform.name]):
                    raise ProjectError(f"Unknown platform '{config[EDefaultConfigSlots.platform.name]}'")

                if not context.project_template.find_toolchain(config[EDefaultConfigSlots.platform.name], config[EDefaultConfigSlots.toolchain.name]):
                    raise ProjectError(f"Unknown toolchain '{config[EDefaultConfigSlots.toolchain.name]}'")

                target_variants = [ arg_variant ]

            else:
                # We have four options
                # - target with config
                # - target with all configs
                # - all targets with config
                # - all targets with all configs

                config_variants = self.pick_variants(context, arg_config)
                target = self.pick_target(context, arg_target)

                # Problem with double/naming of matrices, since per config target files contain config name in them
                if target == EDefaultTargets.All.name:
                    target_variants = list(map(
                        lambda conf_var: f'{target}-{conf_var.config_string}',
                        config_variants
                    ))
                else:
                    target_variants = list(map(
                        lambda conf_var: context.project_template.compile_target_variant_name(ETargetKind.INVALID, target, conf_var.config_string),
                        config_variants
                    ))

            # Refactor context, ensure this makes sense
            emit_context = EmitContext(
                project_template=context.project_template,
                resolved_targets=context.resolved_targets,
                config_matrix=context.config_matrix,
                conan=context.conan,
                mem_fs=None,
                project_fs=None)

            # From fbuild emitter, funcs to find paths and build command strings
            for tar_var in target_variants:
                command_string = FastbuildEmitter.get_fbuild_build_command(emit_context, tar_var)
                logger.Info(f"Building '{tar_var}'...")

                args = command_string.split(' ')
                _, err = call_process_venv(args, context.fs_venv, capture = False, realtime = True, cwd = context.fs_root)
                if err is not None:
                    err_msg = f"FBuild returned error '{err}'"
                    logger.CriticalError(err_msg)
                    raise CompilationError(err_msg)

        except ProjectError:
            raise

        except CompilationError:
            raise

        except Exception as exc:
            logger.Exception(exc)
            raise
