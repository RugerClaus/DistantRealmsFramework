#version 330 core

in vec2 texture_uv;

out vec4 output_color;

uniform sampler2D texture_sampler;
uniform sampler2D light_texture;
uniform float brightness;

void main()
{
    vec4 color = texture(texture_sampler,texture_uv);

    float light = texture(light_texture,texture_uv).r;

    color.rgb *= light;
    color.rgb *= brightness;

    output_color = color;
}