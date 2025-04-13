1. install nodejs:
   - install nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
   - install nodejs: nvm install 22
2. start postgres docker service:
```docker run -d --name postgres \
  -e POSTGRES_PASSWORD=postgres -p 5432:5432 \
  docker.1ms.run/postgres:latest
```
3. init database:
```bash
docker exec -it postgres psql -U postgres
```
```sql
-- 创建数据库
CREATE DATABASE achievement;

-- 连接到新创建的数据库
\c achievement;

-- 创建用户信息 users 表
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- 创建绩效得分 score 表
CREATE TABLE score (
    score_id SERIAL PRIMARY KEY,
    score DECIMAL(10, 2) NOT NULL,
    user_id INT REFERENCES users(user_id)
);

-- 插入示例数据
INSERT INTO users (name, email) VALUES
('张三', 'zs@example.com'),
('李四', 'ls@example.com'),
('王五', 'ww@example.com');

INSERT INTO score (score, user_id) VALUES
(87.75, 1),
(97.50, 2),
(93.25, 3);
```

4. config roo code to connect to the MCP server:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://postgres:postgres@localhost:5432/achievement"
      ]
    }
  }
}
```