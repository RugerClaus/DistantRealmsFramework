#version 330 core

in vec3 fragment_normal;

uniform vec4 color;
uniform vec3 light_direction;
uniform float ambient;

out vec4 FragColor;

void main()
{
    vec3 normal=normalize(fragment_normal);
    vec3 light=normalize(-light_direction);

    float sun_height=max(light.y,0.0);
    float diffuse=max(dot(normal,light),0.0)*sun_height;
    float brightness=ambient+diffuse*(1.0-ambient);

    FragColor=vec4(color.rgb*brightness,color.a);
}