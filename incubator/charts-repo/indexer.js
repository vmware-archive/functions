const Minio = require('minio')
const { exec, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const log = require('winston');
const mutex = require('locks').createMutex();

const minioClient = new Minio.Client({
  endPoint: 'minio-minio-svc',
  port: 9000,
  secure: false,
  accessKey: process.env.MINIO_ACCESS_KEY,
  secretKey: process.env.MINIO_SECRET_KEY,
});

const helmInstall = `
wget -q http://storage.googleapis.com/kubernetes-helm/helm-v2.5.1-linux-amd64.tar.gz
tar xzfv helm-v2.5.1-linux-amd64.tar.gz
/linux-amd64/helm init --client-only
`

execSync(helmInstall, {stdio: 'inherit'});

module.exports = {
  handler: (context) => {
    context = JSON.parse(context);
    let bucket = context.Records[0].s3.bucket.name;
    let package = context.Records[0].s3.object.key;
    let packageDir = fs.mkdtempSync('/tmp/');
    log.info(`Fetching ${package}`);
    minioClient.fGetObject(bucket, package, path.join(packageDir, package), function(err) {
      if (err) {
        return log.error(err);
      }
      mutex.lock(() => {
        log.info(`Acquired lock to process ${package}`);
        minioClient.fGetObject(bucket, 'index.yaml', path.join(packageDir, 'index.yaml'), function(err) {
          let args = '';
          if (err) {
            log.info(`Generating index for the first time with ${package}`);
          } else {
            log.info(`Re-generating index to add ${package}`);
            args = '--merge index.yaml';
          }
          execSync(`/linux-amd64/helm repo index --url ${process.env.REPO_URL} ${args} .`, {stdio: 'inherit', cwd: packageDir});
          log.info(`Uploading regenerated index to bucket`);
          minioClient.fPutObject(bucket, 'index.yaml', path.join(packageDir, 'index.yaml'), 'application/octet-stream', function(err, etag) {
            if (err) {
              return log.error(err);
            }
            execSync(`rm -rf ${packageDir}`, {stdio: 'inherit'});
            log.info(`Successfully uploaded regenerated index`);
            mutex.unlock();
          });
        });
      });
    });
  }
};
