import pygit2 as git
import os
from .stack import Stack, open_stack
from .gitools import get_current_branch, MyRemoteCallback
from .styling import emphasis, warning
from .gh import initGH, GH
from .args import Args

__connections: tuple[git.Repository, Stack, GH] = None

GHIT_STACK_FILENAME = ".ghit.stack"


def stack_filename(repo: git.Repository) -> str:
    repopath = os.path.dirname(os.path.abspath(repo.path))
    return os.path.join(repopath, GHIT_STACK_FILENAME)


def connect(args: Args) -> tuple[git.Repository, Stack, GH]:
    global __connections
    if __connections:
        return __connections
    repo = git.Repository(args.repository)
    if repo.is_empty:
        return repo, Stack(), None
    stack = open_stack(args.stack or stack_filename(repo))
    if not stack:
        stack = Stack()
        current = get_current_branch(repo)
        stack.add_child(current.branch_name)
    __connections = (repo, stack, initGH(repo, stack, args.offline))
    return __connections


def update_upstream(repo: git.Repository, origin: git.Remote, branch: git.Branch):
    full_name = branch.resolve().name
    mrc = MyRemoteCallback()
    origin.push([full_name], callbacks=mrc)
    if not mrc.message:
        # TODO: weak logic?
        branch_ref: str = origin.get_refspec(0).transform(full_name)
        branch.upstream = repo.branches.remote[branch_ref.removeprefix("refs/remotes/")]
        print(
            "Pushed ",
            emphasis(branch.branch_name),
            " to remote ",
            emphasis(origin.url),
            " and set upstream to ",
            emphasis(branch.upstream.branch_name),
            ".",
            sep="",
        )


def sync_branch(
    repo: git.Repository,
    gh: GH,
    origin: git.Remote,
    record: Stack,
    title: str = "",
    draft: bool = False,
):
    branch = repo.branches[record.branch_name]
    if not branch.upstream:
        update_upstream(repo, origin, branch)
    prs = gh.getPRs(record.branch_name)
    if prs and not all(p.closed for p in prs):
        for pr in prs:
            gh.comment(pr)
            gh.update_pr(record, pr)
    else:
        gh.create_pr(record.get_parent().branch_name, record.branch_name, title, draft)


class BadResult(Exception):
    def __init__(
        self, command: str, message: str = "", level=warning, *args: object
    ) -> None:
        super().__init__(*args)
        self.command = command
        self.message = message
        self.level = level
