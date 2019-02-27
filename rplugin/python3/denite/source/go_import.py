# -*- coding: utf-8 -*-

from .base import Base
import denite.util
import subprocess
import tempfile

class Source(Base):
  def __init__(self, vim):
    super().__init__(vim)
    self.name = 'go_import'
    self.kind = Kind(vim)
    self.persist_actions = []

  def gather_candidates(self, context):
    try:
      output = subprocess.run(['gopkgs', '-workDir', '.'], stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as err:
      denite.util.error(self.vim, "command returned invalid response: " + str(err))
      return []

    return [{
      'word': x,
      } for x in output.stdout.decode('utf-8').splitlines()]


class Kind(object):
    def __init__(self, vim):
        self.vim = vim
        self.name = 'go_import'
        self.default_action ='import'
        self.persist_actions = ['preview']
        self.redraw_actions = []

        self._last_preview = {}

    def debug(self, expr):
        denite.util.debug(self.vim, expr)

    def get_action_names(self):
        return ['default'] + [x.replace('action_', '') for x in dir(self)
                              if x.find('action_') == 0]

    def action_import(self, context):
        for target in context['targets']:
            self._import(target['word'])

    def action_godoc(self, context):
        self.vim.call('go#doc#Open', 'new', 'split', context['targets'][0]['word'])

    def action_preview(self, context):
        pass

    def _import(self, name, local_name = ''):
        self.vim.call('go#import#SwitchImport', 1, local_name, name, '')
