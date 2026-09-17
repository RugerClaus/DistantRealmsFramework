#version 330 core

out vec4 output_color;

uniform float time;
uniform vec4 color;

void main()
{
    float pulse = (sin(time) + 1.0) / 2.0;

    output_color = vec4(
        color.rgb,
        color.a
    );
}