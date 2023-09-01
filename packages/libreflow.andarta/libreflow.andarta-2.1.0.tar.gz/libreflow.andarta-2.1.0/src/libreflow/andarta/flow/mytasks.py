import re
import gazu
import pprint
from kabaret import flow
from libreflow.baseflow.mytasks import (
    MyTasks                as BaseMyTasks,
    MyTasksSettings        as BaseMyTasksSettings,
    MyTasksMap             as BaseMyTasksMap,
    TaskItem               as BaseTaskItem
)


class TaskItem(BaseTaskItem):

    episode_name = flow.SessionParam()


class MyTasksMap(BaseMyTasksMap):

    @classmethod
    def mapped_type(cls):
        return TaskItem

    def get_kitsu_tasks(self):
        kitsu_tasks = self._action.kitsu.gazu_api.get_assign_tasks()
        if 'DONE' in self._settings.task_statues_filter.get():
            kitsu_tasks += self._action.kitsu.gazu_api.get_done_tasks()
        
        for i, task_data in enumerate(kitsu_tasks):
            data = {}
          
            # Ignore it if status is not in filter
            if task_data['task_status_short_name'].upper() not in self._settings.task_statues_filter.get():
                continue

            # Regex match for ignore specific entities
            if task_data['task_type_for_entity'] == "Shot":
                seq_regex = re.search(self._settings.sequence_regex.get(), task_data['sequence_name'])
                if seq_regex is None:
                    continue

                sh_regex = re.search(self._settings.shot_regex.get(), task_data['entity_name'])
                if sh_regex is None:
                    continue

            # Set base values
            data.update(dict(
                task_id=task_data['id'],
                task_type=task_data['task_type_name'],
                task_status=task_data['task_status_short_name'],
                entity_id=task_data['entity_id'],
                entity_name=task_data['entity_name'],
                entity_description=task_data['entity_description'],
                shot_frames=None,
                is_bookmarked=False,
                updated_date=task_data['updated_at'],
                episode_name=task_data['episode_name']
            ))

            # Set specific values based on entity type
            if task_data['task_type_for_entity'] == "Shot":
                shot_data = self._action.kitsu.gazu_api.get_shot_data(task_data['entity_name'], task_data['sequence_name'])
                data.update(dict(
                    entity_type=task_data['entity_type_name'],
                    entity_type_name=seq_regex.group(0),
                    shot_frames=shot_data['nb_frames']
                ))
            elif task_data['task_type_for_entity'] == "Asset":
                asset_data = self._action.kitsu.gazu_api.get_asset_data(task_data['entity_name'])
                if asset_data['source_id']:
                    episode_data = gazu.shot.get_episode(asset_data['source_id'])
                    episode_name = episode_data['name']
                else:
                    episode_name = 'MAIN_PACK'

                data.update(dict(
                    episode_name=episode_name,
                    entity_type=task_data['task_type_for_entity'],
                    entity_type_name=task_data['entity_type_name']
                ))

            # Set task name, oid and primary files
            data['dft_task_name'] = self.find_default_task(data['task_type'])
            data['task_oid'], data['primary_files'] = self.set_task_oid(data)

            self._document_cache['task'+str(i)] = data

    def set_task_oid(self, data):
        # Set current project in the oid
        resolved_oid = self.root().project().oid()
        primary_files = None

        # Set values based on entity type
        if data['entity_type'] == 'Shot':
            resolved_oid += '/films/{episode_name}/sequences/{sequence_name}/shots/{shot_name}'.format(
                episode_name=data['episode_name'],
                sequence_name=data['entity_type_name'],
                shot_name=data['entity_name']
            )
        elif data['entity_type'] == 'Asset':
            # episode_name = data['episode_name'] if
            resolved_oid += '/asset_libs/{episode_name}/asset_types/{asset_type_name}/assets/{asset_name}'.format(
                episode_name=data['episode_name'],
                asset_type_name=data['entity_type_name'],
                asset_name=data['entity_name']
            )

        if data['dft_task_name'] is not None:
            resolved_oid += f"/tasks/{data['dft_task_name']}"
            primary_files = self.root().session().cmds.Flow.call(
                resolved_oid, 'get_primary_files', {}, {}
            )
            
        return resolved_oid, primary_files

    def _configure_child(self, child):
        super(MyTasksMap, self)._configure_child(child)
        child.episode_name.set(self._document_cache[child.name()]['episode_name'])


class MyTasksSettings(BaseMyTasksSettings):

    tasks = flow.Child(MyTasksMap)
    sequence_regex = flow.Param('')
    shot_regex = flow.Param('')


class MyTasks(BaseMyTasks):

    settings = flow.Child(MyTasksSettings)

    def _fill_ui(self, ui):
        ui["custom_page"] = "libreflow.andarta.flow.ui.mytasks.MyTasksPageWidget"
