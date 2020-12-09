-- 数据库 schema 信息

/* 
* 任务列表 tlist
*/
CREATE TABLE IF NOT EXISTS tlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- 主键
    target TEXT NOT NULL, -- 目标地点名
    steps INTEGER NOT NULL, -- 步长值，达到目标地点需要走的长度
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP -- 任务创建时间
);