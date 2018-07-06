# -*- coding: utf-8 -*-
import github


class Job():
    """Class defining a complete Job which normally includes clone, build, flash
    and run tests on a device."""
    def __init__(self, payload, user_initiated=False):
        self.payload = payload
        self.user_initiated = user_initiated

    def __str__(self):
        return "{}-{}:{}/{}".format(
                self.pr_id(),
                self.pr_sha1(),
                self.pr_full_name(),
                self.pr_number())

    def pr_number(self):
        return github.pr_number(self.payload)

    def pr_id(self):
        return github.pr_id(self.payload)

    def pr_name(self):
        return github.pr_name(self.payload)

    def pr_full_name(self):
        return github.pr_full_name(self.payload)

    def pr_sha1(self):
        return github.pr_sha1(self.payload)

    def pr_clone_url(self):
        return github.pr_clone_url(self.payload)

    def pr_branch(self):
        return github.pr_branch(self.payload)
