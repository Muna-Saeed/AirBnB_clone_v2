# Redo the task #0 but by using Puppet:

file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure  => 'link',
  target  => '/data/web_static/shared',
  require => File['/data/web_static/releases'],
}

file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  require => File['/data/web_static'],
}

file { '/data/web_static/current/index.html':
  ensure  => 'file',
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  require => File['/data/web_static/current'],
}

class { 'nginx':
  ensure => 'installed',
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'file',
  content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    location / {
        root   /var/www/html;
        index  index.html index.htm;
    }

    location /hbnb_static/ {
        alias  /data/web_static/current/;
    }
}
",
  require => Class['nginx'],
}

service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
