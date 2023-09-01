# Copyright 2021 Vincent Texier
#
# This file is part of MADAM.
#
# MADAM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MADAM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MADAM.  If not, see <https://www.gnu.org/licenses/>.

"""
Madam melt agent module
"""
import json
from datetime import datetime

import adhesive
import jinja2

from madam.adapters.interfaces.agents import AdhesiveApplicationAgentInterface
from madam.domains.applications import Applications
from madam.domains.entities.application import (
    STATUS_ABORTED as APPLICATION_STATUS_ABORTED,
)
from madam.domains.entities.application import (
    STATUS_COMPLETE as APPLICATION_STATUS_COMPLETE,
)
from madam.domains.entities.application import (
    AgentApplication,
    ApplicationAborted,
    ApplicationError,
)
from madam.domains.entities.job import STATUS_COMPLETE, STATUS_ERROR, Job
from madam.domains.entities.workflow_instance import WorkflowInstance
from madam.domains.jobs import Jobs
from madam.libs.serialize import WorkflowInstanceJSONDecoder


class AdhesiveMeltAgent(AdhesiveApplicationAgentInterface):
    """
    AdhesiveMeltAgent class
    """

    AGENT_TYPE = "melt"
    APPLICATIONS = {"melt": AgentApplication("melt", "latest")}

    # pylint: disable=super-init-not-called
    # bug reported, see https://github.com/PyCQA/pylint/issues/4790
    def __init__(self, jobs: Jobs, applications: Applications) -> None:
        """
        Init AdhesiveMeltAgent with domains

        :param jobs: Jobs domain instance
        :param applications: Applications domain instance
        """
        self.jobs = jobs
        self.applications = applications

    def execute(self, context: adhesive.ExecutionToken) -> None:
        """
        Execute application Melt (MLT toolkit) with arguments provided

        Headers:
            arguments:  string with Melt arguments parsed as a jinja2 string
                        (workflow variables can be used with jinja2 tags,
                         see https://jinja.palletsprojects.com/en/3.0.x/templates/#variables)

            applications.melt.version: Optional[string] with version for melt label application

        Example: arguments = "{{source}} -consumer {{destination}}"

        :param context: Adhesive context instance
        :return:
        """
        # job tracking
        workflow_instance: WorkflowInstance = json.loads(
            context.data.madam["workflow_instance"], cls=WorkflowInstanceJSONDecoder
        )
        job = self.jobs.create(
            workflow_instance,
            context.task.id,
            self.AGENT_TYPE,
            context.task.headers,
            context.task.input.as_dict(),
        )

        try:
            # check required headers
            assert job.headers is not None
            assert "arguments" in job.headers, "'arguments' custom header missing"
        except AssertionError as exception:
            # send error status to jobs tracking
            self.jobs.update(
                job, status=STATUS_ERROR, error=str(exception), end_at=datetime.now()
            )
            # stop workflow instance
            raise exception

        try:
            # RUN MELT APPLICATION
            self.application_melt_handler(job)
        except Exception as exception:
            # send error status to jobs tracking
            self.jobs.update(
                job, status=STATUS_ERROR, error=str(exception), end_at=datetime.now()
            )
            # stop workflow instance
            raise exception

        # send success status to jobs tracking
        self.jobs.update(job, status=STATUS_COMPLETE, end_at=datetime.now())

    def application_melt_handler(self, job: Job):
        """
        Run melt application

        :param job: Job instance
        :return:
        """
        if job.headers is None:
            return
        # get command arguments template
        template = jinja2.Template(job.headers["arguments"])
        arguments = template.render(job.input)

        # Melt docker image need the init parameter to be set to True
        docker_config = {"init": True}

        application = self.applications.run(
            job,
            self.APPLICATIONS["melt"].name,
            self.APPLICATIONS["melt"].version
            if "applications.melt.version" not in job.headers
            else job.headers["applications.melt.version"],
            arguments,
            docker_config,
        )

        if application.status == APPLICATION_STATUS_ABORTED:
            raise ApplicationAborted(
                f"Application {application.name} ({application.id}) aborted"
            )
        if application.status != APPLICATION_STATUS_COMPLETE:
            raise ApplicationError(
                application.container_error
                if application.container_error
                else "Application command error, see application logs"
            )
