-- SQL to create templates table
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Sample data for testing
INSERT INTO templates (name, description) VALUES ('Complex Workflow', 'A multi-step workflow for complex tasks');
INSERT INTO templates (name, description) VALUES ('Simple Workflow', 'A basic workflow for simple tasks');