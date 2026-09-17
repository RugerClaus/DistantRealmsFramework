#version 330 core

in vec2 texture_uv;

out vec4 output_color;

uniform sampler2D texture_sampler;

void main()
{
    output_color = texture(texture_sampler, texture_uv);
}