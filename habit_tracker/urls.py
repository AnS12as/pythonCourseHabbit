server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://unix:/home/habit/myproject/habit_tracker.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

