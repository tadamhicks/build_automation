from jenkinsapi.jenkins import Jenkins
from flask import jsonify
from github import Github
import requests
import json


class LastBuild(object):

	def __init__(self, japi, user, pw, proj):

		self.japi = japi
		self.user = user
		self.pw = pw
		self.proj = proj

	def get(self):

		J = Jenkins(self.japi, self.user, self.pw)
		buildNo = J[self.proj].get_last_good_buildnumber()
		response = requests.get(self.japi + '/job/' + self.proj + '/' + str(buildNo) + 
			'/api/python?tree=fingerprint[hash]', 
			auth=(self.user, self.pw))
		json_data = json.loads(response.text)
		checksum = json_data['fingerprint'][0]['hash'].encode()
		return buildNo, checksum

class GH(object):

	def __init__(self, user=None, pw=None, token=None, organization=None, repository, fileage, commitM, content):

		self.user = user
		self.pw = pw
		self.organization = organization
		self.repository = repository
		self.fileage = fileage
		self.commitM = commitM
		self.content = content
		self.token = token

		if not self.token:
			self.g = Github(user, pw)
		else:
			self.g = Github(token)

		if not organization:
			self.repo = g.get_user().get_repo(repository)
		else:
			self.repo = g.get_organization(organization).get_repo(repository)

	def edit_code(self):

		filename = self.repo.get_file_contents(self.fileage)
		response = self.repo.update_file(self.fileage, self.commitM, self.content, filename.sha)
		re_response = {'content': response['content'].path.encode(),
						'commit': response['commit'].sha.encode()}
		return jsonify(re_response)