#version 330 core

layout(location = 0) in vec2 position;
layout(location = 1) in vec2 local_position;

out vec2 frag_local_position;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    frag_local_position = local_position;
}