#version 330 core

in vec2 uv;

uniform sampler2D billboard_texture;
uniform vec3 light_direction;
uniform float ambient;

out vec4 color;

void main()
{
    vec4 texture_color=texture(billboard_texture,uv);

    if(texture_color.a<0.1)
        discard;

    vec3 normal=vec3(0.0,0.0,1.0);
    vec3 light=normalize(-light_direction);

    float diffuse=max(dot(normal,light),0.0);
    float brightness=ambient+diffuse*(1.0-ambient);

    color=vec4(texture_color.rgb*brightness,texture_color.a);
}