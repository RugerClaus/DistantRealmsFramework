#version 330 core

in vec2 uv;

uniform sampler2D billboard_texture;

out vec4 color;

void main()
{
    vec4 texture_color=texture(billboard_texture,uv);

    if(texture_color.a<0.1)
        discard;

    color=vec4(1.0,1.0,1.0,texture_color.a);
}