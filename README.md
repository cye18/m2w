# m2w
Sync Markdown to WordPress posts

> **Note**
> This repository is inspired by and forked from [WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools) with the [author's permission](https://github.com/zhaoolee/WordPressXMLRPCTools/issues/11#issuecomment-1159910760) under GNU General Public License.
> 
> The original repository is used by the author to update his WordPress posts and therefore contains a lot of commits. To make it cleaner, I decided to start a new repository and copy the essential files here.
> 
> Please refer to the original repo for the author's motivation and philosophy of this project

## Quick start
This repository is just a code base. To use it, please go to [m2w-example](https://github.com/cye18/m2w-example) and click "Use thie template" to create a repository for your own WordPress.

In the repo you just created using the template:
1. Add the following GitHub Actions secrets
   1. `USERNAME` your WordPress username
   2. `PASSWORD` your WordPress password
   3. `XMLRPC_PHP` the url of your `xmlrpc.php`. Usually it is `https://your-domain.com/xmlrpc.php`
   4. `M2W_VERSION` the version of m2w (this repo). The latest version is recommended. You can go to [Releases/Tags](https://github.com/cye18/m2w/tags) to find tag name you want to use as well
   5. `ENABLE_DELETION` whether to delete the corresponding WordPress post when the Markdown gets deleted. Feel free to skip it if you don't want to enable deletion
2. Clone the repo to your local and stay on `main` branch
3. Add/modify/delete your post in `posts` directory
4. Commit the changes to GitHub as you did for other repositories
5. Wait for the GitHub Actions to complete
6. **Done!** :tada:

## Tips
- Don't forget to `git pull` when the GitHub Actions is done, since it adds a new commit on GitHub. I sometimes forget about it and commit my changes, then there will be a conflict
- Feel free to modify the README as long as `---start---`, `---end---` and the lines in between are kept untouched