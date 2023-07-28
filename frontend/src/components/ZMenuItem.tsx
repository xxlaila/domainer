import { defineComponent } from 'vue'
import { ElMenuItem, ElIcon, ElSubMenu } from 'element-plus'
import type { MenuProps } from '@/types'

// @ts-ignore
const MenuItem = defineComponent(
  ({ menu }: { menu: MenuProps; key?: any }) => {
    const Title = ({ item }: { item: MenuProps }) => {
      const IconCode = item.icon
      return IconCode ? (
        <>
          <ElIcon>
            {/* @ts-ignore */}
            <IconCode />
          </ElIcon>{' '}
          <span>{item.title}</span>
        </>
      ) : (
        <span>{item.title}</span>
      )
    }

    const Menu = ({ item }: { item: MenuProps }) => (
      <ElMenuItem index={item.path}>{{ title: () => <Title item={item} /> }}</ElMenuItem>
    )

    const SubMenu = ({ item }: { item: MenuProps }) => (
      <ElSubMenu index={item.name}>
        {{
          title: () => <Title item={item} />,
          default: () => (item.children || []).map((child) => <MenuItem menu={child} />)
        }}
      </ElSubMenu>
    )

    return () => (menu.children ? <SubMenu item={menu} /> : <Menu item={menu} />)
  },
  {
    props: ['menu'],
    components: {
      ElMenuItem,
      ElSubMenu,
      ElIcon
    }
  }
)

export default /*#__PURE__*/ MenuItem
